# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "next_quality"
app_title = "Next Quality"
app_publisher = "Dexciss Technology"
app_description = "Module"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "dexciss@gmail.com"
app_license = "MIT"

fixtures = [
    # {"dt":"Custom Field", "filters": [["fieldname", "in", ("release_fence", "search_mode", "priority", "size_minimum", "size_maximum", "customer_pricing_rule_id", "planning_parameters", "column_break_16", "alternate_selection", "column_break_25", "type", "post_op_time", "postop_time", "size_minimum", "size_multiple", "size_maximum", "planning_parameters", "release_fence", "duration", "duration_per_unit", "column_break_66", "search_mode", "priority", "alternate_selection", "type", "c", "location", "available", "type", "column_break_5", "minimum_calendar", "min_interval", "location", "column_break_7", "priority", "fence", "effective_start", "effective_end", "size_minimum", "size_multiple", "size_maximum", "section_break_2", "resource", "resource_quantity", "lead_time", "type", "release_plan", "release_plan_wo", "frepple_po_ref", "column_break_2", "calendar", "release_plan_wo", "frepple_mo_ref", "section_break_15", "warehouse", "type", "constrained", "column_break_21", "efficiency", "maximum_calendar", "available", "maximum", "max_early", "efficiency_calendar")]]}, 
    
    {"dt":"Property Setter", "filters": [["doc_type", "in", ("Item Quality Inspection Parameter", "Job Card", "Quality Inspection Reading", "Quality Inspection", "Work Order")]]}
    ]


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
    "Purchase Receipt": "public/js/purchase_receipt.js",
    "Job Card": "public/js/job_card.js",
    "Item": "public/js/item.js",
    "Material Produce": "public/js/material_produce.js"
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
        "validate":"next_quality.next_quality.custom_quality_inspection.set_inps",
        "before_submit":"next_quality.next_quality.custom_quality_inspection.before_submit",
        "after_insert":"next_quality.next_quality.custom_quality_inspection.set_qc"
    },
    "Sales Order": {
        "before_submit": "next_quality.custom_methods.make_customer_quality_insp_submit_time",
    },
    "Quality Inspection Template": {
       "before_insert":"next_quality.next_quality.custom_quality_inspection_template.before_insert",
    },
    "Material Produce": {
        "before_submit":"next_quality.next_quality.custom_material_produce.before_submit",
        # "on_submit":"next_quality.next_quality.custom_material_produce.on_submit"
    },
    "Job Card":{
        "before_save":"next_quality.next_quality.custom_job_card.make_inprocess_quality_inspection",
    },
    "Batch":{
        "onload":"next_quality.next_quality.custom_batch.set_status"
    },
    "Purchase Receipt":{
        "on_submit":"next_quality.next_quality.custom_purchase_receipt.on_submit",
       # "validate":"next_quality.next_quality.custom_purchase_receipt.validate"
    },
    "Stock Entry":{
        "on_submit": "next_quality.next_quality.custom_stock_entry.on_submit"
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
    "Work Order": "next_quality.next_quality.custom_work_order_dashboard.get_data",
    "Job Card":"next_quality.next_quality.custom_job_card_dashboard.get_data",
    "Purchase Receipt":"next_quality.next_quality.custom_purchase_receipt_dashboard.get_data",
    # "Material Produce":"next_quality.next_quality.custom_material_produce_dashboard.get_data"

}

# jenv = {
#     "methods": [
#         "get_details:nextquality.next_quality.custom_sales_invoice.get_details"
#     ]
#
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]



user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

