# Copyright (c) 2026, JSPL and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class BlanketBookingOrderItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		allow_overvaluation: DF.Check
		base_rate: DF.Currency
		item_group: DF.Link
		ordered_qty: DF.Float
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		qty: DF.Float
		rate: DF.Currency
		terms_and_conditions: DF.Text | None
	# end: auto-generated types

	pass
