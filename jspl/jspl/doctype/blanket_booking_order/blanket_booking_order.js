// Copyright (c) 2026, JSPL and contributors
// For license information, please see license.txt

frappe.ui.form.on("Blanket Booking Order", {
	setup: function (frm) {
		frm.add_fetch("customer", "customer_name", "customer_name");
		frm.add_fetch("supplier", "supplier_name", "supplier_name");
	},

	onload: function (frm) {
		frm.trigger("set_tc_name_filter");
	},

	refresh: function (frm) {
		erpnext.hide_company(frm);
	},

	tc_name: function (frm) {
		erpnext.utils.get_terms(frm.doc.tc_name, frm.doc, function (r) {
			if (!r.exc) {
				frm.set_value("terms", r.message);
			}
		});
	},

	set_tc_name_filter: function (frm) {
		if (frm.doc.order_type === "Selling") {
			frm.set_value("supplier", "");
			frm.set_query("tc_name", function () {
				return { filters: { selling: 1 } };
			});
		}
		if (frm.doc.order_type === "Purchasing") {
			frm.set_value("customer", "");
			frm.set_query("tc_name", function () {
				return { filters: { buying: 1 } };
			});
		}
	},

	order_type: function (frm) {
		frm.trigger("set_tc_name_filter");
	},

	conversion_rate: function (frm) {
		(frm.doc.items || []).forEach((item) => set_base_rate(frm, item));
		frm.refresh_field("items");
	},
});

frappe.ui.form.on("Blanket Booking Order Item", {
	rate: function (frm, cdt, cdn) {
		set_base_rate(frm, frappe.get_doc(cdt, cdn));
		frm.refresh_field("items");
	},
});

function set_base_rate(frm, item) {
	frappe.model.round_floats_in(item, ["rate"]);
	let base_rate = flt(flt(item.rate) * flt(frm.doc.conversion_rate), precision("base_rate", item));
	frappe.model.set_value(item.doctype, item.name, "base_rate", base_rate);
}
