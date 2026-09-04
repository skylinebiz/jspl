# Copyright (c) 2026, JSPL and contributors
# For license information, please see license.txt

import frappe


def before_uninstall():
	"""Remove the Custom Fields this app added (module "JSPL" only) so
	uninstalling it doesn't leave orphaned fields - e.g. `custom_blanket_booking_order`
	on Purchase Order Item / Sales Order Item - behind on other doctypes."""
	custom_field_names = frappe.get_all("Custom Field", filters={"module": "JSPL"}, pluck="name")
	for name in custom_field_names:
		frappe.delete_doc("Custom Field", name, ignore_permissions=True, force=True)
