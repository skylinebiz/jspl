# Copyright (c) 2026, JSPL and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.query_builder.functions import Sum
from frappe.utils import flt, getdate

from erpnext import get_company_currency
from erpnext.controllers.accounts_controller import validate_conversion_rate
from erpnext.controllers.queries import item_query
from erpnext.setup.utils import get_exchange_rate


class BlanketBookingOrder(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from jspl.jspl.doctype.blanket_booking_order_item.blanket_booking_order_item import (
			BlanketBookingOrderItem,
		)

		amended_from: DF.Link | None
		company: DF.Link
		conversion_rate: DF.Float
		currency: DF.Link
		customer: DF.Link | None
		customer_name: DF.Data | None
		from_date: DF.Date
		items: DF.Table[BlanketBookingOrderItem]
		naming_series: DF.Literal["JSPL-BBO-.YYYY.-"]
		order_date: DF.Date | None
		order_no: DF.Data | None
		order_type: DF.Literal["", "Selling", "Purchasing"]
		supplier: DF.Link | None
		supplier_name: DF.Data | None
		tc_name: DF.Link | None
		terms: DF.TextEditor | None
		to_date: DF.Date
	# end: auto-generated types

	def before_validate(self):
		self.set_currency()
		self.set_conversion_rate()

	def validate(self):
		self.validate_dates()
		self.validate_duplicate_item_groups()
		self.validate_item_qty()
		self.set_base_rates()

	def set_currency(self):
		if self.currency:
			return

		party_type, party = self.get_party()
		party_currency = frappe.get_cached_value(party_type, party, "default_currency") if party else None
		self.currency = party_currency or get_company_currency(self.company)

	def get_party(self):
		if self.order_type == "Selling":
			return "Customer", self.customer
		return "Supplier", self.supplier

	def set_conversion_rate(self):
		company_currency = get_company_currency(self.company)
		if self.currency == company_currency:
			self.conversion_rate = 1.0
		elif not self.conversion_rate and self.order_type:
			exchange_rate_type = "for_selling" if self.order_type == "Selling" else "for_buying"
			self.conversion_rate = get_exchange_rate(
				self.currency, company_currency, self.from_date, exchange_rate_type
			)

		validate_conversion_rate(
			self.currency,
			self.conversion_rate,
			self.meta.get_translated_label("conversion_rate"),
			self.company,
		)
		self.conversion_rate = flt(self.conversion_rate, self.precision("conversion_rate"))

	def validate_dates(self):
		if getdate(self.from_date) > getdate(self.to_date):
			frappe.throw(_("From date cannot be greater than To date"))

	def validate_duplicate_item_groups(self):
		item_group_list = []
		for item in self.items:
			if item.item_group in item_group_list:
				frappe.throw(
					_("Note: Item Group {0} added multiple times").format(frappe.bold(item.item_group))
				)
			item_group_list.append(item.item_group)

	def validate_item_qty(self):
		for d in self.items:
			if flt(d.qty) < 0:
				frappe.throw(_("Row {0}: Quantity cannot be negative.").format(d.idx))

	def set_base_rates(self):
		for item in self.items:
			rate = flt(item.rate, item.precision("rate"))
			item.rate = rate
			item.base_rate = flt(rate * flt(self.conversion_rate), item.precision("base_rate"))

	def update_ordered_qty(self):
		"""Recompute each row's Ordered Quantity from submitted Purchase Orders
		whose items are linked to this Blanket Booking Order (via the
		`custom_blanket_booking_order` field on Purchase Order Item), aggregated
		by Item Group. Called from the Purchase Order `on_submit`/`on_cancel`
		hooks below, so a cancelled Purchase Order's quantity is dropped
		automatically (it's no longer docstatus 1)."""
		if self.order_type != "Purchasing":
			return

		po = frappe.qb.DocType("Purchase Order")
		po_item = frappe.qb.DocType("Purchase Order Item")

		item_group_qty = frappe._dict(
			(
				frappe.qb.from_(po_item)
				.join(po)
				.on(po.name == po_item.parent)
				.select(po_item.item_group, Sum(po_item.stock_qty).as_("qty"))
				.where(
					(po_item.custom_blanket_booking_order == self.name)
					& (po.docstatus == 1)
					& (po.status != "Closed")
				)
				.groupby(po_item.item_group)
			).run()
		)

		for d in self.items:
			d.db_set("ordered_qty", item_group_qty.get(d.item_group, 0))


def validate_purchase_order(doc, method=None):
	"""Purchase Order `before_submit` hook: every Blanket Booking Order picked
	on this order's items must be a submitted, Purchasing BBO for the same
	supplier, must actually list the item's Item Group, and the quantity
	being booked against that Item Group (across this order) must not exceed
	the BBO row's remaining quantity (plus the Buying Settings allowance)."""
	bbo_names = {d.custom_blanket_booking_order for d in doc.items if d.custom_blanket_booking_order}
	if not bbo_names:
		return

	allowance = flt(frappe.db.get_single_value("Buying Settings", "blanket_order_allowance"))

	for bbo_name in bbo_names:
		bbo = frappe.get_doc("Blanket Booking Order", bbo_name)
		if bbo.docstatus != 1:
			frappe.throw(_("{0} must be submitted").format(frappe.bold(bbo_name)))
		if bbo.order_type != "Purchasing":
			frappe.throw(_("{0} is not a Purchasing Blanket Booking Order").format(frappe.bold(bbo_name)))
		if bbo.supplier != doc.supplier:
			frappe.throw(
				_("Supplier of {0} does not match the Supplier of this Purchase Order").format(
					frappe.bold(bbo_name)
				)
			)

		bbo_rows = {d.item_group: d for d in bbo.items}
		item_group_qty = {}
		for item in doc.items:
			if item.custom_blanket_booking_order != bbo_name:
				continue
			if item.item_group not in bbo_rows:
				frappe.throw(
					_("Row {0}: Item Group {1} is not listed in {2}").format(
						item.idx, frappe.bold(item.item_group), frappe.bold(bbo_name)
					)
				)
			item_group_qty[item.item_group] = item_group_qty.get(item.item_group, 0) + flt(
				item.stock_qty or item.qty
			)

		for item_group, qty in item_group_qty.items():
			bbo_row = bbo_rows[item_group]
			remaining_qty = flt(bbo_row.qty) - flt(bbo_row.ordered_qty)
			allowed_qty = remaining_qty + (remaining_qty * (allowance / 100))
			if bbo_row.qty and qty > allowed_qty:
				frappe.throw(
					_("Item Group {0} cannot be ordered more than {1} against {2}.").format(
						frappe.bold(item_group), allowed_qty, frappe.bold(bbo_name)
					)
				)


def update_bbo_ordered_qty(doc, method=None):
	"""Purchase Order `on_submit`/`on_cancel` hook: refresh Ordered Quantity on
	every Blanket Booking Order referenced by this order's items."""
	bbo_names = {d.custom_blanket_booking_order for d in doc.items if d.custom_blanket_booking_order}
	for bbo_name in bbo_names:
		frappe.get_doc("Blanket Booking Order", bbo_name).update_ordered_qty()


@frappe.whitelist()
def bbo_item_query(doctype, txt, searchfield, start, page_len, filters):
	"""Item link query for Purchase Order Item's `item_code`. Same as ERPNext's
	own `item_query`, except when the row's `custom_blanket_booking_order` is
	passed in `filters`, results are further restricted to Items whose Item
	Group is one of that Blanket Booking Order's Item Groups."""
	if isinstance(filters, str):
		filters = frappe.parse_json(filters)
	filters = dict(filters or {})

	bbo_name = filters.pop("blanket_booking_order", None)
	if bbo_name:
		item_groups = list(
			set(
				frappe.get_all(
					"Blanket Booking Order Item", filters={"parent": bbo_name}, pluck="item_group"
				)
			)
		)
		filters["item_group"] = ["in", item_groups or [""]]

	return item_query(doctype, txt, searchfield, start, page_len, filters)
