# Copyright (c) 2013, Dexciss Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
	columns=get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters):
	columns=[
			{
				"label": _("Name"),
				"fieldname": "name",
				"fieldtype": "Data",
				"width": 140
			},
			{
				"label": _("Item Code"),
				"fieldname": 'item_code',
				"fieldtype": "Link",
				"options": "Item",
				"width": 100
			},
			{
				"label": _("Item Name"),
				"fieldname": 'item_name',
				"fieldtype": "Read Only",
				"width": 100
			},

			{
				"label": _("Item Description"),
				"fieldname": 'description',
				"fieldtype": "Read Only",
				"width": 100
			},
			{
				"label": _("Quality Inspection Template"),
				"fieldname": 'quality_inspection_template',
				"fieldtype": "Link",
				"options":"Quality Inspection Template",
				"width": 100
			},
			{
				"label": _("Qty To Manufacture"),
				"fieldname": 'qty',
				"fieldtype": "Float",
				"width": 100
			},
			{
				"label": _("Batch Number"),
				"fieldname": 'batch_no',
				"fieldtype": "Data",
				"width": 100
			},
			{
				"label": _("Serial Number"),
				"fieldname": 'serial_no',
				"fieldtype": "Data",
				"width": 100
			},
			{
				"label": _("Document Status"),
				"fieldname": 'status',
				"fieldtype": "Select",
				"width": 100
			},
			{
				"label": _("Quality Status"),
				"fieldname": 'status1',
				"fieldtype": "Select",
				"width": 100
			},
	]
	return columns

def get_condition(filters):

	conditions=" "
	if filters.get("from_date"):
		conditions += " AND ip.report_date>='%s'" % filters.get('from_date')
	if filters.get("to_date"):
		conditions += " AND ip.report_date<='%s'" % filters.get('to_date')
	if filters.get("item_code"):
		conditions += "AND ip.item_code = '%s'" % filters.get('item_code')
	if filters.get("purchase_receipt"):
		conditions += "AND p.name = '%s'" % filters.get('purchase_receipt')
	if filters.get("batch_no"):
		conditions += "AND ip.batch_no = '%s'" % filters.get('batch_no')
	return conditions


def get_data(filters):
	if filters.tree_type == 'Purchase Reciept':
		conditions = get_condition(filters)
		doc = frappe.db.sql("""select p.name ,ip.item_code,ip.item_name,ip.description,ip.quality_inspection_template,p.total_qty as qty,
									ip.batch_no,ip.item_serial_no,p.status as status1,ip.status From `tabPurchase Receipt` p,
									`tabQuality Inspection` ip where ip.reference_name=p.name and ip.status != 'Completed' and ip.inspection_type = 'Incoming' {conditions} """.format(conditions=conditions),filters, as_dict=1)
		return doc
	
