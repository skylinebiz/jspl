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

		if (frm.doc.docstatus !== 1 || !frm.has_perm("submit")) {
			return;
		}

		if (frm.doc.status === "On Hold") {
			frm.add_custom_button(__("Resume"), () => update_bbo_status(frm, "Resume"), __("Status"));
		} else if (frm.doc.status === "Closed") {
			frm.add_custom_button(__("Re-open"), () => update_bbo_status(frm, "Re-open"), __("Status"));
		} else if (frm.doc.status !== "Completed") {
			// A Completed BBO has nothing left to Hold/Close against.
			frm.add_custom_button(__("Hold"), () => hold_bbo(frm), __("Status"));
			frm.add_custom_button(__("Close"), () => update_bbo_status(frm, "Closed"), __("Status"));
		}
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

function hold_bbo(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __("Reason for Hold"),
		fields: [
			{
				fieldname: "reason_for_hold",
				fieldtype: "Text",
				reqd: 1,
			},
		],
		primary_action_label: __("Hold"),
		primary_action: function () {
			const data = dialog.get_values();
			frappe.call({
				method: "frappe.desk.form.utils.add_comment",
				args: {
					reference_doctype: frm.doctype,
					reference_name: frm.docname,
					content: __("Reason for hold: {0}", [frappe.utils.escape_html(data.reason_for_hold)]),
					comment_email: frappe.session.user,
					comment_by: frappe.session.user_fullname,
				},
				callback: function (r) {
					if (!r.exc) {
						dialog.hide();
						update_bbo_status(frm, "On Hold");
					}
				},
			});
		},
	});
	dialog.show();
}

function update_bbo_status(frm, status) {
	frappe.call({
		method: "jspl.jspl.doctype.blanket_booking_order.blanket_booking_order.update_bbo_status",
		args: { name: frm.doc.name, status: status },
		freeze: true,
		callback: function (r) {
			if (!r.exc) {
				frm.reload_doc();
			}
		},
	});
}
