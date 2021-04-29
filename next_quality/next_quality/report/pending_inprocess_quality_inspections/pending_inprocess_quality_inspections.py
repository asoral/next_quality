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
				"fieldtype": "Link",
				"options": "Work Order",
				"width": 140
			},
			{
				"label": _("Item Code"),
				"fieldname": 'production_item',
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
				"fieldname": 'inprocess_quality_inspection_template',
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
				"label": _("BOM"),
				"fieldname": 'bom_no',
				"fieldtype": "Link",
				"options":"BOM",
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
		conditions += "AND ip.creation>='%s'" % filters.get('from_date')
	if filters.get("to_date"):
		conditions += " AND ip.modified<='%s'" % filters.get('to_date')
	if filters.get("item_code"):
		conditions += "AND w.production_item = '%s'" % filters.get('item_code')
	if filters.get("work_order"):
		conditions += "AND w.name = '%s'" % filters.get('work_order')
	if filters.get("job_card"):
		conditions += "AND j.name = '%s'" % filters.get('job_card')
	if filters.get("batch_no"):
		conditions += " ip.batch_no = '%s'" % filters.get('batch_no')
	return conditions


def get_data(filters):
	if filters.tree_type == 'Work Order':
		conditions=get_condition(filters)
		doc=frappe.db.sql("""select distinct w.name ,w.production_item,w.item_name,ip.inprocess_quality_inspection_template,w.qty,
							w.bom_no,w.status 
							From `tabWork Order` w 
		 					join `tabWork InProcess Quality Inspection Template` ip 
							on ip.parent=w.name
							left outer join `tabQuality Inspection` q
		 					on w.name=q.reference_name Where w.status!="Completed"
		 					{conditions} """.format(conditions=conditions),filters, as_dict=1)
		return doc
	elif filters.tree_type == 'Job Card':
		conditions = get_condition(filters)
		doc=frappe.db.sql("""select distinct j.name ,j.production_item,j.item_name,ip.inprocess_quality_inspection_template,j.for_quantity as qty,
							j.bom_no,j.status 
							From `tabJob Card` j 
		 					inner join `tabWork InProcess Quality Inspection Template` ip 
							on ip.parent=j.name
							left outer join `tabQuality Inspection` q
		 					on j.name=q.reference_name Where j.status!="Completed"
		 					{conditions} """.format(conditions=conditions),filters, as_dict=1)
		return doc
	
