app_name = "jspl"
app_title = "JSPL"
app_publisher = "Harshit Jain."
app_description = "JSPL"
app_email = "harshit@skylinebiz.in"
app_license = "mit"

# Apps
# ------------------

required_apps = ["erpnext"]

# Fixtures
# ------------------
# Records synced into every site on `bench migrate`, and re-exported here on
# `bench export-fixtures`.

fixtures = [
	{
		"doctype": "Custom Field",
		"filters": [
            ["module", "in", ["JSPL"]]
        ]
	}
]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "jspl",
# 		"logo": "/assets/jspl/logo.png",
# 		"title": "JSPL",
# 		"route": "/jspl",
# 		"has_permission": "jspl.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/jspl/css/jspl.css"
# app_include_js = "/assets/jspl/js/jspl.js"

# include js, css files in header of web template
# web_include_css = "/assets/jspl/css/jspl.css"
# web_include_js = "/assets/jspl/js/jspl.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "jspl/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Purchase Order": "public/js/purchase_order.js",
	"Sales Order": "public/js/sales_order.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "jspl/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "jspl.utils.jinja_methods",
# 	"filters": "jspl.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "jspl.install.before_install"
# after_install = "jspl.install.after_install"

# Uninstallation
# ------------

before_uninstall = "jspl.uninstall.before_uninstall"
# after_uninstall = "jspl.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "jspl.utils.before_app_install"
# after_app_install = "jspl.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "jspl.utils.before_app_uninstall"
# after_app_uninstall = "jspl.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "jspl.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "jspl.notifications.get_notification_config"

# Awesome Bar
# -----------
# Extra search results: list of dicts with label, description, route, index.
# route: ["List", "ToDo"], "/desk/docs/some/page", or "https://example.com"
# awesomebar_search = ["jspl.search.awesomebar_results"]

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Purchase Order": {
		"before_validate": "jspl.jspl.doctype.blanket_booking_order.blanket_booking_order.apply_bbo_rate",
		"before_submit": "jspl.jspl.doctype.blanket_booking_order.blanket_booking_order.validate_order_against_bbo",
		"on_submit": "jspl.jspl.doctype.blanket_booking_order.blanket_booking_order.update_bbo_ordered_qty",
		"on_cancel": "jspl.jspl.doctype.blanket_booking_order.blanket_booking_order.update_bbo_ordered_qty",
	},
	"Sales Order": {
		"before_validate": "jspl.jspl.doctype.blanket_booking_order.blanket_booking_order.apply_bbo_rate",
		"before_submit": "jspl.jspl.doctype.blanket_booking_order.blanket_booking_order.validate_order_against_bbo",
		"on_submit": "jspl.jspl.doctype.blanket_booking_order.blanket_booking_order.update_bbo_ordered_qty",
		"on_cancel": "jspl.jspl.doctype.blanket_booking_order.blanket_booking_order.update_bbo_ordered_qty",
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"jspl.tasks.all"
# 	],
# 	"daily": [
# 		"jspl.tasks.daily"
# 	],
# 	"hourly": [
# 		"jspl.tasks.hourly"
# 	],
# 	"weekly": [
# 		"jspl.tasks.weekly"
# 	],
# 	"monthly": [
# 		"jspl.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "jspl.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "jspl.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "jspl.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "jspl.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["jspl.utils.before_request"]
# after_request = ["jspl.utils.after_request"]

# Job Events
# ----------
# before_job = ["jspl.utils.before_job"]
# after_job = ["jspl.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"jspl.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

