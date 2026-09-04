// Copyright (c) 2026, JSPL and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sales Order", {
	setup: function (frm) {
		// Blanket Booking Order picked against a Sales Order Item must be
		// submitted, Selling, for the same customer as this order, and its
		// validity (From Date - To Date) must cover this order's Transaction Date.
		frm.set_query("custom_blanket_booking_order", "items", function (doc) {
			return {
				filters: {
					order_type: "Selling",
					customer: doc.customer,
					docstatus: 1,
					from_date: ["<=", doc.transaction_date],
					to_date: [">=", doc.transaction_date],
				},
			};
		});

		// Once a row has a Blanket Booking Order, only Items whose Item Group
		// is listed on that BBO may be picked for that row - so two rows on
		// the same Sales Order, against two different BBOs, each only see
		// their own BBO's Item Groups. Mirrors ERPNext's own default filters
		// (see erpnext/public/js/utils/sales_common.js) and adds to them.
		frm.set_query("item_code", "items", function (doc, cdt, cdn) {
			const row = locals[cdt][cdn];
			const filters = { is_sales_item: 1, customer: doc.customer, has_variants: 0 };

			if (row.custom_blanket_booking_order) {
				filters.blanket_booking_order = row.custom_blanket_booking_order;
			}

			return {
				query: "jspl.jspl.doctype.blanket_booking_order.blanket_booking_order.bbo_item_query",
				filters: filters,
			};
		});
	},

	customer: function (frm) {
		clear_bbo_from_items(frm);
	},
});

// A row's Blanket Booking Order is only ever valid for the Customer it was
// filtered against (see `custom_blanket_booking_order`'s query above) - if
// the Customer changes, every row's selection is stale and must be cleared.
function clear_bbo_from_items(frm) {
	let cleared = false;
	(frm.doc.items || []).forEach((item) => {
		if (item.custom_blanket_booking_order) {
			frappe.model.set_value(item.doctype, item.name, "custom_blanket_booking_order", "");
			cleared = true;
		}
	});
	if (cleared) {
		frappe.show_alert({
			message: __("Blanket Booking Order cleared from items - Customer changed."),
			indicator: "orange",
		});
	}
}

frappe.ui.form.on("Sales Order Item", {
	custom_blanket_booking_order: function (frm, cdt, cdn) {
		sync_row_with_bbo(cdt, cdn);
	},

	item_code: function (frm, cdt, cdn) {
		sync_row_with_bbo(cdt, cdn);
	},
});

// Prefills the row's Rate from the matching Blanket Booking Order Item as
// soon as both are known, purely for immediate feedback - the authoritative
// override happens server-side (see `apply_bbo_rate`) on every save, so the
// rate can never drift from what was committed on the BBO.
function sync_row_with_bbo(cdt, cdn) {
	const row = locals[cdt][cdn];
	const bbo_name = row.custom_blanket_booking_order;
	const item_group = row.item_group;
	if (!bbo_name || !item_group) {
		return;
	}

	frappe.db
		.get_value(
			"Blanket Booking Order Item",
			{ parent: bbo_name, item_group: item_group },
			"rate",
			null,
			"Blanket Booking Order"
		)
		.then((r) => {
			if (r.exc) {
				// A real error (e.g. permissions) - don't clear the row over it.
				return;
			}
			if (!r.message || r.message.rate === undefined) {
				frappe.model.set_value(cdt, cdn, "custom_blanket_booking_order", "");
				frappe.msgprint(
					__("Item Group {0} is not listed in {1} - please choose a matching Blanket Booking Order.", [
						frappe.utils.escape_html(item_group),
						frappe.utils.escape_html(bbo_name),
					])
				);
				return;
			}
			frappe.model.set_value(cdt, cdn, "rate", r.message.rate);
		});
}
