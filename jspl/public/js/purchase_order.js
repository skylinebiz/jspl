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
	},
});
