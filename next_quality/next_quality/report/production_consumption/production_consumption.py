# Copyright (c) 2013, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	# chart = get_chart_data()
	return columns, data, None 



def get_columns(filters):
	return [
		{"label": _("Work Order"), "fieldname": "work_order", "fieldtype": "Link", "options": "Work Order", "width": 150},
		{"label": _("Prod. Item "), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 120},
		{"label": _("Prod. Item Name"), "fieldname": "production_item", "fieldtype": "Data", "width": 120},
		{"label": _("Stock Entry"), "fieldname": "name", "fieldtype": "Link", "options": "Stock Entry", "width": 150},
		{ "label": _("Consumption ID"), "fieldname": "material_consumption", "fieldtype": "Data",  "width": 120 },
		{ "label": _("Production ID"), "fieldname": "material_produce", "fieldtype": "Data", "width": 120 },
		{"label": _("Company ID"), "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 120},
		{"label": _("Prod. Item Group"), "fieldname": "item_group", "fieldtype": "Data", "width": 120},
		{"label": _("Prod. Brand"), "fieldname": "brand", "fieldtype": "Data", "width": 100},
		{"label": _("FG Inspection"), "fieldname": "name1", "fieldtype": "Link", "options": "Quality Inspection", "width": 120},
		{"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
		{"label": _("Trx. Type"), "fieldname": "trxtype", "fieldtype": "Data", "width": 120},
		{"label": _("Target Warehouse"), "fieldname": "t_warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
		{"label": _("Item"), "fieldname": "item_no_stock_entry", "fieldtype": "Data", "width": 120},
		{"label": _("Serial No"), "fieldname": "serial_no", "fieldtype": "Data", "width": 120},
		{"label": _("Batch"), "fieldname": "batch_no", "fieldtype": "Data", "width": 120},
		{"label": _("Quantity"), "fieldname": "qty", "fieldtype": "Data", "width": 120},
		{"label": _("UOM"), "fieldname": "uom", "fieldtype": "Data", "width": 120},
		{"label": _("Qty as per Stock UOM"), "fieldname": "transfer_qty", "fieldtype": "Data", "width": 120},
		{"label": _("Stock UOM"), "fieldname": "stock_uom", "fieldtype": "Data", "width": 120},
		{"label": _("Amount"), "fieldname": "amount", "fieldtype": "Data", "width": 120},
		{"label": _("Valuation Rate"), "fieldname": "valuation_rate", "fieldtype": "Data", "width": 120},
		{"label": _("Cost"), "fieldname": "basic_rate", "fieldtype": "Data", "width": 120},
		{"label": _("Actual yeild"), "fieldname": "actual_yeild", "fieldtype": "Percentage", "width": 120},
		{"label": _("Yeild Deviation"), "fieldname": "yeild_deviation", "fieldtype": "Percentage", "width": 120},
		# { "label": _("Source Warehouse"), "fieldname": "s_warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150 },
		# { "label": _("Type"), "fieldname": "stock_entry_type", "fieldtype": "Data", "width": 120 },

	]

def get_data(filters):
	data = []
	query = """
		SELECT 
			se.work_order,
			wo.production_item,
			i.item_group,
			i.brand,
			se.name,
			qi.name as name1,
			se.posting_date,
			CASE
				WHEN sed.s_warehouse IS NOT NULL AND sed.t_warehouse IS NULL THEN 'Consumed'
				WHEN sed.s_warehouse IS NULL AND sed.t_warehouse IS NOT NULL THEN 'Produced'
			END as trxtype,
			CASE
				WHEN sed.s_warehouse IS NOT NULL AND sed.t_warehouse IS NULL THEN sed.s_warehouse
				WHEN sed.s_warehouse IS NULL AND sed.t_warehouse IS NOT NULL THEN sed.t_warehouse
			END as warehouse,
			se.material_consumption,
			se.material_produce,
			sed.item_code,
			sed.item_name,
			sed.batch_no,
			sed.serial_no,
			sed.qty,
			se.company,
			sed.uom,
			sed.transfer_qty,
			sed.stock_uom,
			sed.basic_rate,
			sed.amount,
			sed.valuation_rate,
			wo.actual_yeild,
			wo.yeild_deviation
		FROM 
			`tabStock Entry` se
		INNER JOIN `tabStock Entry Detail` sed ON sed.parent = se.name
		INNER JOIN `tabWork Order` wo ON se.work_order = wo.name
		INNER JOIN `tabItem` i ON wo.production_item = i.name
		LEFT JOIN `tabQuality Inspection` qi ON qi.reference_name = wo.name AND qi.docstatus = 1
		WHERE 
			se.stock_entry_type IN ('Material Consumption for Manufacture', 'Manufacture')
			AND se.docstatus = 1
			{conditions}
		ORDER BY se.posting_date DESC
	"""

	conditions, values = get_conditions(filters)
	query = query.format(conditions=conditions)

	q_data = frappe.db.sql(query, values=values, as_dict=True)
	for row in q_data:
		data.append({
			"work_order": row.work_order,
			"name": row.name,
			"posting_date": row.posting_date,
			"material_consumption": row.material_consumption,
			"material_produce": row.material_produce,
			"item_code": row.production_item,
			"item_group": row.item_group,
			"brand": row.brand,
			"t_warehouse": row.warehouse,
			"company": row.company,
			"serial_no": row.serial_no,
			"batch_no": row.batch_no,
			"name1": row.name1,
			"qty": row.qty,
			"uom": row.uom,
			"basic_rate": row.basic_rate,
			"production_item": row.item_name,
			"item_no_stock_entry": row.item_code,
			"stock_uom": row.stock_uom,
			"transfer_qty": row.transfer_qty,
			"amount": row.amount,
			"valuation_rate": row.valuation_rate,
			"trxtype": row.trxtype,
			"actual_yeild": row.actual_yeild,
			"yeild_deviation": row.yeild_deviation,
		})
	return data

def get_conditions(filters):
	conditions = []
	values = {}

	if filters.get('item_code'):
		conditions.append("wo.production_item = %(item_code)s")
		values["item_code"] = filters['item_code']
	if filters.get('serial_number'):
		conditions.append("sed.serial_no = %(serial_number)s")
		values["serial_number"] = filters['serial_number']
	if filters.get('batch_number'):
		conditions.append("sed.batch_no = %(batch_number)s")
		values["batch_number"] = filters['batch_number']
	if filters.get('item_group'):
		conditions.append("i.item_group = %(item_group)s")
		values["item_group"] = filters['item_group']
	if filters.get('brand'):
		conditions.append("i.brand = %(brand)s")
		values["brand"] = filters['brand']
	if filters.get('company'):
		conditions.append("se.company = %(company)s")
		values["company"] = filters['company']
	if filters.get('warehouse'):
		conditions.append("sed.t_warehouse = %(warehouse)s")
		values["warehouse"] = filters['warehouse']
	if filters.get('work_order'):
		conditions.append("se.work_order = %(work_order)s")
		values["work_order"] = filters['work_order']
	if filters.get("from_date"):
		conditions.append("se.posting_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("se.posting_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]

	# Group by removed since it doesn’t work in current logic without aggregation

	return " AND " + " AND ".join(conditions) if conditions else "", values



# def get_chart_data():
# 	# New chart 
#     query = """
#         SELECT
#             sed.item_name,
#             SUM(sed.transfer_qty)
#         FROM
#             `tabStock Entry` se
#         JOIN
#             `tabStock Entry Detail` sed ON sed.parent = se.name
#         WHERE
#             se.docstatus = 1
#             AND se.stock_entry_type IN ('Material Consumption for Manufacture', 'Manufacture')
#             AND sed.s_warehouse IS NULL
#         GROUP BY
#             sed.item_name
#         ORDER BY
#             SUM(sed.transfer_qty) DESC
#         LIMIT 30
#     """

#     data = frappe.db.sql(query)
#     labels = [d[0] for d in data]
#     values = [d[1] for d in data]

#     chart = {
#         "data": {
#             "labels": labels,
#             "datasets": [{
#                 "name": _("Item"),
#                 "values": values
#             }]
#         },
#         "type": "bar"
#     }
#     return chart

 



