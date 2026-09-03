// Copyright (c) 2026, JSPL and contributors
// For license information, please see license.txt

frappe.ui.form.on("Purchase Order", {
	setup: function (frm) {
		// Blanket Booking Order picked against a Purchase Order Item must be
		// submitted, Purchasing, and for the same supplier as this order.
		frm.set_query("custom_blanket_booking_order", "items", function (doc) {
			return {
				filters: {
					order_type: "Purchasing",
					supplier: doc.supplier,
					docstatus: 1,
				},
			};
		});

		// Once a row has a Blanket Booking Order, only Items whose Item Group
		// is listed on that BBO may be picked for that row - so two rows on
		// the same Purchase Order, against two different BBOs, each only see
		// their own BBO's Item Groups. Mirrors ERPNext's own default filters
		// (see erpnext/public/js/controllers/buying.js) and adds to them.
		frm.set_query("item_code", "items", function (doc, cdt, cdn) {
			const row = locals[cdt][cdn];
			let filters;
			if (doc.is_subcontracted) {
				filters = { supplier: doc.supplier };
				if (doc.is_old_subcontracting_flow) {
					filters.is_sub_contracted_item = 1;
				} else {
					filters.is_stock_item = 0;
				}
			} else {
				filters = { supplier: doc.supplier, is_purchase_item: 1, has_variants: 0 };
			}

			if (row.custom_blanket_booking_order) {
				filters.blanket_booking_order = row.custom_blanket_booking_order;
			}

			return {
				query: "jspl.jspl.doctype.blanket_booking_order.blanket_booking_order.bbo_item_query",
				filters: filters,
			};
		});
	},
});

frappe.ui.form.on("Purchase Order Item", {
	custom_blanket_booking_order: function (frm, cdt, cdn) {
		validate_item_group_against_bbo(frm, cdt, cdn);
	},

	item_code: function (frm, cdt, cdn) {
		validate_item_group_against_bbo(frm, cdt, cdn);
	},
});

function validate_item_group_against_bbo(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	const bbo_name = row.custom_blanket_booking_order;
	const item_group = row.item_group;
	if (!bbo_name || !item_group) {
		return;
	}

	frappe.db
		.get_list("Blanket Booking Order Item", {
			filters: { parent: bbo_name, item_group: item_group },
			limit: 1,
		})
		.then((matches) => {
			if (!matches.length) {
				frappe.model.set_value(cdt, cdn, "custom_blanket_booking_order", "");
				frappe.msgprint(
					__("Item Group {0} is not listed in {1} - please choose a matching Blanket Booking Order.", [
						frappe.utils.escape_html(item_group),
						frappe.utils.escape_html(bbo_name),
					])
				);
			}
		});
}
