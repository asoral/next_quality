# Copyright (c) 2013, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	chart = get_chart_data()
	return columns, data, None, chart


def get_columns(filters):
	columns = [
		{
			"label": _("Work Order"),
			"fieldname": "work_order",
			"fieldtype": "Link",
			"options": "Work Order",
			"width": 150
		},

		{
			"label": _("Prod. Item "),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 120
		},
		{
			"label": _("Prod. Item Name"),
			"fieldname": "production_item",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Consumption ID"),
			"fieldname":"material_consumption",
			"fieldtype": "Link",
			"options": "Material Consumption",
			"width": 120
		},
		{
			"label": _("Production ID"),
			"fieldname": "material_produce",
			"fieldtype": "Link",
			"options": "Material Produce",
			"width": 120
		},
		{
			"label": _("Stock Entry"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Stock Entry",
			"width": 150
		},
		{
			"label": _("Company ID"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 120
		},
		{
			"label": _("Prod. Item Group"),
			"fieldname": "item_group",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Prod. Brand"),
			"fieldname": "brand",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("FG Inspection"),
			"fieldname": "name1",
			"fieldtype": "Link",
			"options": "Quality Inspection",
			"width": 120
		},
		{
			"label": _("Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 120
		},
		# {
		#     "label": _("Type"),
		#     "fieldname": "stock_entry_type",
		#     "fieldtype": "Data",
		#     "width": 120
		# },
		{
			"label": _("Trx. Type"),
			"fieldname": "trxtype",
			"fieldtype": "Data",
			"width": 120
		},

		# {
		#     "label": _("Source Warehouse"),
		#     "fieldname": "s_warehouse",
		#     "fieldtype": "Link",
		#     "options": "Warehouse",
		#     "width": 150
		# },
		{
			"label": _("Target Warehouse"),
			"fieldname": "t_warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 150
		},
		{
			"label": _("Item"),
			"fieldname": "item_no_stock_entry",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Serial No"),
			"fieldname": "serial_no",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Batch"),
			"fieldname": "batch_no",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Quantity"),
			"fieldname": "qty",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("UOM"),
			"fieldname": "uom",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Qty as per Stock UOM"),
			"fieldname": "transfer_qty",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Stock UOM"),
			"fieldname": "stock_uom",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Amount"),
			"fieldname": "amount",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Valuation Rate"),
			"fieldname": "valuation_rate",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Cost"),
			"fieldname": "basic_rate",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Actual yeild"),
			"fieldname": "actual_yeild",
			"fieldtype": "Percentage",
			"width": 120
		},
		{
			"label": _("Yeild Deviation"),
			"fieldname": "yeild_deviation",
			"fieldtype": "Percentage",
			"width": 120
		},
		# {
		# 	"label": _("WorkOrder"),
		# 	"fieldname": "work_n",
		# 	"fieldtype": "Link",
		# 	"options": "Work Order",
		# 	"width": 150
		# },



	]
	return columns


def get_data(filters):
	# print("======")
	data = []
	conditions = get_conditions(filters)
	a = int(conditions.count("group by work_order"))
	b = int(conditions.count("group by trxtype"))
	query = """select 
    se.work_order,
    wo.production_item,
    i.item_group as FGGroup,
    i.brand as 'FG Brand',
    se.name as 'SE Voucher',
    qi.name as name1,
    se.posting_date as 'Posting Date',
    se.posting_time as 'Posting Time',
    case
    when sed.s_warehouse is not null and sed.t_warehouse is null then 'Consumed'
    when sed.s_warehouse is null and sed.t_warehouse is not null then 'Produced'
    end as 'Trx. Type',
    case
    when sed.s_warehouse is not null and sed.t_warehouse is null then sed.s_warehouse
    when sed.s_warehouse is null and sed.t_warehouse is not null then sed.t_warehouse
    end as 'Warehouse',
    se.material_consumption as 'Consumption ID',
    se.material_produce as 'Production ID',
    sed.item_code as Item,
    sed.item_name as 'Item Name',
    sed.batch_no as 'Batch No.',
    sed.serial_no as 'Serial No',
    sed.qty,
	se.company as 'Company ID',
    sed.uom,
    sed.transfer_qty as 'Qty in Stock UOM',
    sed.stock_uom as 'Stock UOM',
    sed.basic_rate,
    sed.basic_amount,
    sed.additional_cost,
    sed.amount,
    sed.valuation_rate,
	wo.actual_yeild,
	wo.yeild_deviation
    
    

	from 
    `tabStock Entry` as se
    inner join `tabStock Entry Detail` as sed on sed.parent = se.name
    inner join `tabWork Order` as wo on se.work_order = wo.name
    inner join `tabItem` as i on wo.production_item = i.name
    left outer join `tabQuality Inspection` as qi on qi.reference_name = wo.name and qi.docstatus = 1
	where 
    se.stock_entry_type in ('Material Consumption for Manufacture', 'Manufacture')
    and se.docstatus = 1
	"""
	# cond = ""
	if filters.tree_type == 'Work Order':
		cond = ""
		work_order = """ select distinct se.work_order from `tabStock Entry` se where se.stock_entry_type in("Manufacture",'Material Consumption for Manufacture') and se.docstatus = 1 and se.work_order != "" """
		p_work_order = frappe.db.sql(work_order)
		count = len(p_work_order)
		# print("*******",p_work_order)
		for p in p_work_order:
			# data = []
			row = {
				"work_order": p[0]
			}
			data.append(row)
			order_by="""order by sed.modified desc,se.posting_date desc, wo.name , wo.production_item"""
			cond = """ and  se.work_order = '%s'""" % p[0]
			q_data = frappe.db.sql(query +cond+conditions+order_by )
			# data = []
			# row = {
			#     "work_order": p[0]
			# }
			# data.append(row)
			for q in q_data:
				row = {
					"name": q[4],
					"posting_date": q[6],
					"stock_entry_type": q[0],
					"material_consumption":q[10],
					"material_produce":q[11],
					"item_code": q[1],
					"item_group": q[2],
					# "s_warehouse": q[13],
					"t_warehouse": q[9],
					"company":q[17],
					"serial_no": q[15],
					"batch_no": q[14],
					"name1":q[5],
					"qty": q[16],
					"uom": q[20],
					"basic_rate": q[21],
					"brand": q[3],
					"production_item":q[13],
					"item_no_stock_entry":q[12],
					"stock_uom":q[20],
					"transfer_qty":q[19],
					"amount":q[24],
					"valuation_rate":q[25],
					"trxtype": q[8],
					"actual_yeild":q[26],
					"yeild_deviation":q[27]

				}
				data.append(row)
		return data
	# return [data for _ in range(count)]

	#

	elif filters.tree_type == 'Prod. Item':
		cond = ""
		trxtype = """ select distinct wo.production_item from `tabWork Order` wo,`tabStock Entry` se where wo.name = se.work_order and se.stock_entry_type in ("Manufacture",'Material Consumption for Manufacture') and wo.docstatus = 1 """
		p_trxtype = frappe.db.sql(trxtype)
		# print("&&&&&",p_trxtype)
		for p in p_trxtype:
			# cond += """ and  b.production_item = '%s' order by b.modified desc """ % p[0]
			query = """ select
			se.work_order,
			wo.production_item,
			i.item_group as FGGroup,
			i.brand as 'FG Brand',
			se.name as 'SE Voucher',
			qi.name as 'FG Inspection',
			se.posting_date as 'Posting Date',
			se.posting_time as 'Posting Time',
			case
			when sed.s_warehouse is not null and sed.t_warehouse is null then 'Consumed'
			when sed.s_warehouse is null and sed.t_warehouse is not null then 'Produced'
			end as 'Trx. Type',
			case
			when sed.s_warehouse is not null and sed.t_warehouse is null then sed.s_warehouse
			when sed.s_warehouse is null and sed.t_warehouse is not null then sed.t_warehouse
			end as 'Warehouse',
			se.material_consumption as 'Consumption ID',
			se.material_produce as 'Production ID',
			sed.item_code as Item,
			sed.item_name as 'Item Name',
			sed.batch_no as 'Batch No.',
			sed.serial_no as 'Serial No',
			se.company as 'Company ID',
			sed.qty,
			sed.uom,
			sed.transfer_qty as 'Qty in Stock UOM',
			sed.stock_uom as 'Stock UOM',
			sed.basic_rate,
			sed.basic_amount,
			sed.additional_cost,
			sed.amount,
			sed.valuation_rate,
			wo.actual_yeild,
			wo.yeild_deviation
			
			

			from 
			`tabStock Entry` as se
			inner join `tabStock Entry Detail` as sed on sed.parent = se.name
			inner join `tabWork Order` as wo on se.work_order = wo.name
			inner join `tabItem` as i on wo.production_item = i.name
			left outer join `tabQuality Inspection` as qi on qi.reference_name = wo.name and qi.docstatus = 1
			where 
			se.stock_entry_type in ('Material Consumption for Manufacture', 'Manufacture')
			and se.docstatus = 1
						"""
			row = {
				"item_code": p[0]
			}
			data.append(row)
			order_by="""order by sed.modified desc ,se.posting_date desc, wo.name , wo.production_item"""
			cond = """ and  wo.production_item = '%s' """ % p[0]
			q_data = frappe.db.sql(query + cond +conditions+order_by)
			for q in q_data:
				row = {
					"name": q[4],
					"posting_date": q[6],
					"work_order": q[0],
					"material_consumption":q[10],
					"material_produce":q[11],
					"item_code": q[1],
					"item_group": q[2],
					# "s_warehouse": q[13],
					"t_warehouse": q[9],
					"company":q[16],
					"serial_no": q[15],
					"batch_no": q[14],
					"name1":q[5],
					"qty": q[17],
					"uom": q[20],
					"basic_rate": q[21],
					"brand": q[3],
					"production_item":q[13],
					"item_no_stock_entry":q[12],
					"stock_uom":q[20],
					"transfer_qty":q[19],
					"amount":q[24],
					"valuation_rate":q[25],
					"trxtype": q[8],
					"actual_yeild":q[26],
					"yeild_deviation":q[27]

				}
				data.append(row)

		return data
	# else:
	# 	query = """ select
	# 		se.work_order,
	# 		wo.production_item,
	# 		i.item_group as FGGroup,
	# 		i.brand as 'FG Brand',
	# 		se.name as 'SE Voucher',
	# 		qi.name as 'FG Inspection',
	# 		se.posting_date as 'Posting Date',
	# 		se.posting_time as 'Posting Time',
	# 		case
	# 		when sed.s_warehouse is not null and sed.t_warehouse is null then 'Consumed'
	# 		when sed.s_warehouse is null and sed.t_warehouse is not null then 'Produced'
	# 		end as 'Trx. Type',
	# 		case
	# 		when sed.s_warehouse is not null and sed.t_warehouse is null then sed.s_warehouse
	# 		when sed.s_warehouse is null and sed.t_warehouse is not null then sed.t_warehouse
	# 		end as 'Warehouse',
	# 		se.material_consumption as 'Consumption ID',
	# 		se.material_produce as 'Production ID',
	# 		sed.item_code as Item,
	# 		sed.item_name as 'Item Name',
	# 		sed.batch_no as 'Batch No.',
	# 		sed.serial_no as 'Serial No',
	# 		sed.qty,
	# 		sed.uom,
	# 		sed.transfer_qty as 'Qty in Stock UOM',
	# 		sed.stock_uom as 'Stock UOM',
	# 		sed.basic_rate,
	# 		sed.basic_amount,
	# 		sed.additional_cost,
	# 		sed.amount,
	# 		sed.valuation_rate,
	# 		se.company as 'Company ID',
	# 		wo.actual_yeild,
	# 		wo.yeild_deviation

	# 		from 
	# 		`tabStock Entry` as se
	# 		inner join `tabStock Entry Detail` as sed on sed.parent = se.name
	# 		inner join `tabWork Order` as wo on se.work_order = wo.name
	# 		inner join `tabItem` as i on wo.production_item = i.name
	# 		left outer join `tabQuality Inspection` as qi on qi.reference_name = wo.name and qi.docstatus = 1
	# 		where 
	# 		se.stock_entry_type in ('Material Consumption for Manufacture', 'Manufacture')
	# 		and se.docstatus = 1

					

	# 				"""
	# 	# and d.item_code = c.item_code
	# 	# group by work_order
	# 	# print("====query",query+conditions)
	# 	order_by = """ order by se.posting_date desc, wo.name , wo.production_item"""
	# 	q_data = frappe.db.sql(query + conditions + order_by)
	# 	data = []
	# 	for q in q_data:
	# 		row = {
	# 				"name": q[4],
	# 				"posting_date": q[6],
	# 				"work_order": q[0],
	# 				"material_consumption":q[10],
	# 				"material_produce":q[11],
	# 				"item_code": q[1],
	# 				"item_group": q[2],
	# 				# "s_warehouse": q[13],
	# 				"t_warehouse": q[9],
	# 				"company":q[25],
	# 				"serial_no": q[15],
	# 				"batch_no": q[14],
	# 				"name1":q[5],
	# 				"qty": q[16],
	# 				"uom": q[17],
	# 				"basic_rate": q[20],
	# 				"brand": q[3],
	# 				"production_item":q[13],
	# 				"item_no_stock_entry":q[12],
	# 				"stock_uom":q[19],
	# 				"transfer_qty":q[18],
	# 				"amount":q[23],
	# 				"valuation_rate":q[20],
	# 				"trxtype": q[8],
	# 		}
	# 		data.append(row)

	# 	return data


def get_conditions(filters):
	
	if filters:
		query = """ """
		# and stock_entry_type = 'Manufacture'
		if filters.get('item_code'):
			query += """ and wo.production_item = '%s'  """ % filters.item_code
		if filters.get('serial_number'):
			query += """ and sed.serial_no = '%s'  """ % filters.serial_number
		if filters.get('batch_number'):
			query += """ and sed.batch_no = '%s'  """ % filters.batch_number
		if filters.get('item_group'):
			query += """ and  i.item_group = '%s'  """ % filters.item_group
		if filters.get('brand'):
			query += """ and i.brand = '%s'  """ % filters.brand
		if filters.get('company'):
			query += """and se.company = '%s'  """ % filters.company
		if filters.get('warehouse'):
			query += """ and sed.t_warehouse = '%s'  """ % filters.warehouse
		if filters.get('work_order'):
			query += """ and se.work_order = '%s'  """ % filters.work_order
		if filters.get("from_date"):
			query += "and se.posting_date>='%s'" % filters.get('from_date')
		if filters.get("to_date"):
			query += " and se.posting_date<='%s'" % filters.get('to_date')
		if filters.get('group_by'):
			if filters.get("group_by") == 'manufacture':
				query += """ group by work_order """ 
		if filters.get('group_by'):
			if filters.get("group_by") == 'trxtype':
				query += """group by trxtype"""
	return query


def get_chart_data():
	query = """ select distinct
			sed.item_name as "Item:Data:120"
			from 
				`tabStock Entry` se, `tabStock Entry Detail` sed
			where
					sed.parent = se.name
				and se.docstatus = 1
				and se.stock_entry_type in ('Material Consumption for Manufacture', 'Manufacture')
				and sed.s_warehouse is null
				"""

	q_data = frappe.db.sql(query)
	labels = []
	value = []
	for q in q_data:
		labels.append(q[0])
		query2 = """ select SUM(transfer_qty)
				from 
					`tabStock Entry` se, `tabStock Entry Detail` sed
				where

						sed.parent = se.name
						and se.stock_entry_type in ('Material Consumption for Manufacture', 'Manufacture')
						and se.docstatus = 1
					"""
		query2 += """ and  sed.item_name = '%s'  """ % q[0]
		testvalue = frappe.db.sql(query2)
		value.append(testvalue[0])
	# value = ["12","13"]
	# print("**********************************##", value)
	datasets = []
	if value:
		datasets.append({'name': _('Item'), 'values': value})
	chart = {
		"data": {
			'labels': labels,
			'datasets': datasets
		}
	}
	chart["type"] = "bar"
	return chart

