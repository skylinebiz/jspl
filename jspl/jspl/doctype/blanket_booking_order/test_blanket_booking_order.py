# Copyright (c) 2026, JSPL and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, today

test_dependencies = ["Item Group", "Company", "Currency"]


class TestBlanketBookingOrder(FrappeTestCase):
	def test_duplicate_item_group_not_allowed(self):
		bbo = frappe.get_doc(
			{
				"doctype": "Blanket Booking Order",
				"order_type": "Selling",
				"company": "_Test Company",
				"currency": "INR",
				"from_date": today(),
				"to_date": add_days(today(), 30),
				"items": [
					{"item_group": "All Item Groups", "qty": 10, "rate": 100},
					{"item_group": "All Item Groups", "qty": 5, "rate": 100},
				],
			}
		)
		self.assertRaises(frappe.ValidationError, bbo.insert)

	def test_from_date_after_to_date_not_allowed(self):
		bbo = frappe.get_doc(
			{
				"doctype": "Blanket Booking Order",
				"order_type": "Selling",
				"company": "_Test Company",
				"currency": "INR",
				"from_date": today(),
				"to_date": add_days(today(), -1),
				"items": [{"item_group": "All Item Groups", "qty": 10, "rate": 100}],
			}
		)
		self.assertRaises(frappe.ValidationError, bbo.insert)
