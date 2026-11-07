# -*- coding: utf-8 -*-
from . import __version__ as app_version

app_name = "next_quality"
app_title = "Next Quality"
app_publisher = "Dexciss Technology"
app_description = "Module"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "dexciss@gmail.com"
app_license = "MIT"

fixtures = []


# include js, css files in header of desk.html
# app_include_css = "/assets/nextquality/css/nextquality.css"
# app_include_js = "/assets/js/qc_templates.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/nextquality/css/nextquality.css"
# web_include_js = "/assets/nextquality/js/nextquality.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "nextquality/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Quality Inspection": "public/js/quality_inspection.js",
    "Quality Inspection Template": "public/js/quality_inspection_template.js",
    "Sales Order": "public/js/sales_order.js",
    "Pick List": "public/js/pick_list.js",
    "Delivery Note": "public/js/delivery_note.js",
    "Customer": "public/js/customer.js",
    "Stock Entry": "public/js/stock_entry.js",
    "Work Order" : "public/js/work_order.js",
    # "Purchase Receipt": "public/js/purchase_receipt.js",
    "Job Card": "public/js/job_card.js",
    "Item": "public/js/item.js",
    "Batch":"public/js/batch.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "nextquality.install.before_install"
# after_install = "nextquality.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "nextquality.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Quality Inspection":"next_quality.next_quality.custom_quality_inspection.CustomQualityInspection"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Quality Inspection": {
        "on_submit": "next_quality.next_quality.custom_quality_inspection.set_insepection_in_batch",
        "before_save":"next_quality.next_quality.custom_quality_inspection.before_save",
        # "after_save":"next_quality.next_quality.custom_quality_inspection.after_save",
        "validate":"next_quality.next_quality.custom_quality_inspection.set_inps",
        "before_submit":"next_quality.next_quality.custom_quality_inspection.before_submit",
        "after_insert":["next_quality.next_quality.custom_quality_inspection.set_qc",
                        "next_quality.next_quality.custom_quality_inspection.set_supplier"],
        "on_trash":"next_quality.next_quality.custom_stock_entry.delete_quality_inspection"
    },
    "Sales Order": {
        "before_submit": "next_quality.custom_methods.make_customer_quality_insp_submit_time",
    },
    "Quality Inspection Template": {
        "before_insert":"next_quality.next_quality.custom_quality_inspection_template.before_insert",
        # "before_save":"next_quality.next_quality.custom_quality_inspection_template.before_save",

    },
    "Job Card":{
        "before_save":"next_quality.next_quality.custom_job_card.make_inprocess_quality_inspection",
    },
    "Batch":{
        "onload":"next_quality.next_quality.custom_batch.set_status"
    },
    # "Purchase Receipt":{
        # "on_submit":"next_quality.next_quality.custom_purchase_receipt.on_submit",
    #     # "validate":"next_quality.next_quality.custom_purchase_receipt.validate"
    # },
    "Stock Entry":{
        "on_submit": [
            # "next_quality.next_quality.custom_stock_entry.on_submit",
            "next_quality.next_quality.custom_stock_entry.submit_quality_inspection","next_quality.next_quality.custom_quality_inspection.set_insepection_in_batch_from_stock_entry"],
        "validate":"next_quality.next_quality.custom_stock_entry.create_quality_insp"
    },
    "Delivery Note":{
        "before_submit": "next_quality.next_quality.custom_delivery_note.get_list"
    },
    "Work Order":{
        "before_save":"next_quality.next_quality.custom_work_order.validate_Qc",
        "on_submit":"next_quality.next_quality.custom_work_order.submit_job_card",
        # "on_submit":"next_quality.next_quality.custom_work_order.timelogs_data"
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {

    # "all": [
	#  "nextquality.next_quality.custom_work_order.periodic_quality_inspection"
	#  ],
	# "daily": [
	# 	"nextquality.tasks.daily"
	# ],
	"hourly": [
		"next_quality.next_quality.custom_work_order.periodic_quality_inspection",
        "next_quality.next_quality.custom_job_card.periodic_quality_inspect",
	 ],
    # "cron": {
	# 	"0/1 * * * *": [
	# 		"nextquality.next_quality.custom_work_order.periodic_quality_inspection"
	# 	]
	# },
	# "weekly": [
	# 	"nextquality.tasks.weekly"
	# ],
	# "monthly": [
	# 	"nextquality.tasks.monthly"
	# ]
}

# Testing
# -------

# before_tests = "nextquality.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
    # "erpnext/stock/doctype/quality_inspection/quality_inspection.update_qc_reference": "next_quality/next_quality/custom_quality_inspection.update_qc_reference"

}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {
	"Customer": "next_quality.next_quality.custom_customer_dashboard.get_data",
    "Sales Order": "next_quality.sales_order_dashboard.get_data",
    #"Work Order": "next_quality.next_quality.custom_work_order_dashboard.get_data",
    # "Material Produce":"next_quality.next_quality.custom_material_produce_dashboard.get_data"

}

# jenv = {
#     "methods": [
#         "get_jinja_data:next_quality.custom_sales_invoice.get_jinja_data"
#     ]

# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Desk navigation (Frappe v16): Apps screen entry. The sidebars and dock ship as
# <module>/sidebar/*, <module>/workspace/* and dock/next_quality/next_quality.json
app_logo_url = "/assets/next_quality/images/next_quality-logo.svg"
app_home = "/desk/next-quality"

add_to_apps_screen = [
	{
		"name": "next_quality",
		"logo": "/assets/next_quality/images/next_quality-logo.svg",
		"title": "Next Quality",
		"route": app_home,
		"has_permission": "next_quality.navigation.check_app_permission",
	}
]

# Install / uninstall
# -------------------
# Custom fields and property setters are defined in next_quality/constants/custom_fields.py.
# They are created on install and on every migrate, and removed when the app is uninstalled.
after_install = "next_quality.setup.install.after_install"
after_migrate = "next_quality.setup.install.after_migrate"
before_uninstall = "next_quality.setup.uninstall.before_uninstall"
