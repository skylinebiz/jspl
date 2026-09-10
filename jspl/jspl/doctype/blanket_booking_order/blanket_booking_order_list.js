// Copyright (c) 2026, JSPL and contributors
// For license information, please see license.txt

frappe.listview_settings["Blanket Booking Order"] = {
	add_fields: ["status"],

	get_indicator: function (doc) {
		const status_colors = {
			Draft: "gray",
			"To Order": "orange",
			"Partially Ordered": "yellow",
			Completed: "green",
			"On Hold": "blue",
			Closed: "purple",
			Cancelled: "red",
		};

		return [
			__(doc.status),
			status_colors[doc.status] || "gray",
			"status,=," + doc.status,
		];
	},
};
