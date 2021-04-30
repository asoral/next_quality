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
			"label": _("Stock Entry"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Stock Entry",
			"width": 150
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
		}



	]
	return columns


def get_data(filters):
	# print("======")
	data = []
	conditions = get_conditions(filters)
	a = int(conditions.count("group by work_order"))
	b = int(conditions.count("group by trxtype"))
	query = """ select
					a.name as  "Stock Entry:Data:150",
					a.posting_date as "Date: Date: 120",
					a.stock_entry_type as "Type: Link: 120",
					a.work_order as "Work Order:Link:150",
					b.item_name as "Item: Link: 120",
					c.item_group as "Item Group: Data: 120",
					c.s_warehouse as "Source Warehouse:Link:150",
					c.t_warehouse as "Target Warehouse:Link:150",
					c.serial_no as "Serial No: Data:120",
					c.batch_no as "Batch:Data:120",
					c.qty as "Quantity: Float: 120",
					c.uom as "UOM: Link: 120",
					c.basic_rate as "Cost: Data: 120",
					d.brand as "Brand: Data: 100",
					b.production_item as "Production Item:Data:120",
					c.item_name as "Item:Data:120",
					c.stock_uom as "Stock UOM:Data:120",
					c.transfer_qty as "Qty as per Stock UOM:Data:120",
					c.amount as "Amount:Data:120",
					c.valuation_rate as "Valuation Rate:Data:120",                     
					case
					when c.s_warehouse is null then 'Produced'
					else 'Consumed'
					end as "Trx. Type: Data: 120"

					from
						`tabStock Entry` a, `tabWork Order` b, `tabStock Entry Detail` c, `tabItem` d
					where
						a.work_order = b.name
						and a.stock_entry_type = "Manufacture"
						and c.parent = a.name
						and d.item_code = c.item_code
						and a.docstatus = 1

					"""
	# cond = ""
	if a > 0:
		cond = ""
		work_order = """ select distinct a.work_order from `tabStock Entry` a where a.stock_entry_type = "Manufacture" and a.docstatus = 1 and a.work_order != "" """
		p_work_order = frappe.db.sql(work_order)
		count = len(p_work_order)
		# print("*******",p_work_order)
		for p in p_work_order:
			print("Pppp", p[0])
			# data = []
			row = {
				"work_order": p[0]
			}
			data.append(row)
			cond = """ and  a.work_order = '%s' order by b.modified desc """ % p[0]

			print("cond--", cond)
			q_data = frappe.db.sql(query + cond)
			print("q_data_--", q_data)
			# data = []
			# row = {
			#     "work_order": p[0]
			# }
			# data.append(row)
			for q in q_data:
				row = {
					"name": q[0],
					"posting_date": q[1],
					"stock_entry_type": q[2],
					"item_code": q[14],
					"item_group": q[5],
					"s_warehouse": q[6],
					"t_warehouse": q[7],
					"serial_no": q[8],
					"batch_no": q[9],
					"qty": q[10],
					"uom": q[11],
					"basic_rate": q[12],
					"brand": q[13],
					"production_item": q[14]+":"+q[4],
					"item_no_stock_entry":q[15],
					"stock_uom":q[16],
					"transfer_qty":q[17],
					"amount":q[18],
					"valuation_rate":q[19],
					"trxtype": q[20]
				}
				data.append(row)
		return data
	# return [data for _ in range(count)]

	#

	elif b > 0:
		cond = ""
		trxtype = """ select distinct a.production_item from `tabWork Order` a,`tabStock Entry` c where a.name = c.work_order and c.stock_entry_type = "Manufacture" and a.docstatus = 1 """
		p_trxtype = frappe.db.sql(trxtype)
		# print("&&&&&",p_trxtype)
		for p in p_trxtype:
			# cond += """ and  b.production_item = '%s' order by b.modified desc """ % p[0]
			query = """ select
				a.name as  "Stock Entry:Data:150",
				a.posting_date as "Date:Date:120",
				a.stock_entry_type as "Type:Link:120",
				a.work_order as "Work Order:Link:150",
				b.item_name as "Item:Link:120",
				c.item_group as "Item Group:Data:120",
				c.s_warehouse as "Source Warehouse:Link:150",
				c.t_warehouse as "Target Warehouse:Link:150",
				c.serial_no as "Serial No:Data:120",
				c.batch_no as "Batch:Data:120",
				c.qty as "Quantity:Float:120",
				c.uom as "UOM:Link:120",
				c.basic_rate as "Cost:Data:120",
				d.brand as "Brand:Data:100",
				b.production_item as "Production Item:Data:120",
				c.item_name as "Item:Data:120",
				c.stock_uom as "Stock UOM:Data:120",
				c.transfer_qty as "Qty as per Stock UOM:Data:120",
				c.amount as "Amount:Data:120",
				c.valuation_rate as "Valuation Rate:Data:120",               
				case
				when c.s_warehouse is null then 'Produced'
				else 'Consumed'
				end as "TrxType: Data: 120"

				from
					`tabStock Entry` a, `tabWork Order` b, `tabStock Entry Detail` c, `tabItem` d
				where
					a.work_order = b.name
					and a.stock_entry_type = "Manufacture"
					and c.parent = a.name
					and d.item_name = c.item_name
					and a.docstatus = 1
					and b.docstatus = 1

				"""
			row = {
				"item_code": p[0]
			}
			data.append(row)
			cond = """ and  b.production_item = '%s' order by b.modified desc """ % p[0]
			q_data = frappe.db.sql(query + cond)
			for q in q_data:
				row = {
					"name": q[0],
					"posting_date": q[1],
					"stock_entry_type": q[2],
					"work_order": q[3],
					# "item_code": q[14],
					"item_group": q[5],
					"s_warehouse": q[6],
					"t_warehouse": q[7],
					"serial_no": q[8],
					"batch_no": q[9],
					"qty": q[10],
					"uom": q[11],
					"basic_rate": q[12],
					"brand": q[13],
					"production_item":q[14]+":"+q[4],
					"item_no_stock_entry":q[15],
					"stock_uom":q[16],
					"transfer_qty":q[17],
					"amount":q[18],
					"valuation_rate":q[19],
					"trxtype": q[20]

				}
				data.append(row)

		return data
	else:
		query = """ select 
			a.name as  "Stock Entry:Data:150",
			a.posting_date as "Date: Date: 120",
			a.stock_entry_type as "Type: Link: 120",
			a.work_order as "Work Order:Link:150",
			b.item_name as "Item: Link: 120",
			d.item_group as "Item Group: Data: 120",
			c.s_warehouse as "Source Warehouse:Link:150",
			c.t_warehouse as "Target Warehouse:Link:150",
			c.serial_no as "Serial No: Data:120",
			c.batch_no as "Batch:Data:120",
			c.qty as "Quantity: Float: 120",
			c.uom as "UOM: Link: 120",
			c.basic_rate as "Cost: Data: 120",
			d.brand as "Brand: Data: 100",
			b.production_item as "Production Item:Data:120",
			c.item_name as "Item:Data:120",
			c.stock_uom as "Stock UOM:Data:120",
			c.transfer_qty as "Qty as per Stock UOM:Data:120",
			c.amount as "Amount:Data:120",
			c.valuation_rate as "Valuation Rate:Data:120",
			
			case
			when c.s_warehouse is null then 'Produced'
			else 'Consumed'
			end as "TrxType: Data: 120"

			from 
				`tabStock Entry` a, `tabWork Order` b, `tabStock Entry Detail` c, `tabItem` d
			where
				a.work_order = b.name
				and a.stock_entry_type = "Manufacture"
				and c.parent = a.name
			and d.item_name = b.item_name
			and a.docstatus = 1

			"""
		# and d.item_code = c.item_code
		# group by work_order
		# print("====query",query+conditions)
		order_by = """ order by b.modified desc """
		q_data = frappe.db.sql(query + conditions + order_by)
		data = []
		for q in q_data:
			row = {
				"name": q[0],
				"posting_date": q[1],
				"stock_entry_type": q[2],
				"work_order": q[3],
				"item_code": q[14],
				"item_group": q[5],
				"s_warehouse": q[6],
				"t_warehouse": q[7],
				"serial_no": q[8],
				"batch_no": q[9],
				"qty": q[10],
				"uom": q[11],
				"basic_rate": q[12],
				"brand": q[13],
				"production_item": q[14]+":"+q[4],
				"item_no_stock_entry":q[15],
				"stock_uom":q[16],
				"transfer_qty":q[17],
				"amount":q[18],
				"valuation_rate":q[19],
				"trxtype": q[20 ]
			}
			data.append(row)

		return data


def get_conditions(filters):
	
		query = """ """
		# and stock_entry_type = 'Manufacture'
		if filters.get('item_code'):
			query += """ and  b.production_item = '%s'  """ % filters.item_code
		if filters.get('serial_number'):
			query += """ and  serial_no = '%s'  """ % filters.serial_number
		if filters.get('batch_number'):
			query += """ and  batch_no = '%s'  """ % filters.batch_number
		if filters.get('item_group'):
			query += """ and  c.item_group = '%s'  """ % filters.item_group
		if filters.get('brand'):
			query += """ and  brand = '%s'  """ % filters.brand
		if filters.get('s_warehouse'):
			query += """ and  s_warehouse = '%s'  """ % filters.s_warehouse
		if filters.get('t_warehouse'):
			query += """ and  t_warehouse = '%s'  """ % filters.t_warehouse
		if filters.get('group_by'):
			if filters.get("group_by") == 'manufacture':
				query += """ group by work_order """
		if filters.get('group_by'):
			if filters.get("group_by") == 'trxtype':
				query += """group by trxtype"""
		return query


def get_chart_data():
	query = """ select distinct
			c.item_name as "Item:Data:120"
			from 
				`tabStock Entry` a, `tabStock Entry Detail` c
			where
					c.parent = a.name
				and a.docstatus = 1
				and a.stock_entry_type = "Manufacture"
				and c.s_warehouse is null
				"""

	q_data = frappe.db.sql(query)
	labels = []
	value = []
	for q in q_data:
		labels.append(q[0])
		query2 = """ select SUM(transfer_qty)
				from 
					`tabStock Entry` a, `tabStock Entry Detail` c
				where

						c.parent = a.name
						and a.stock_entry_type = "Manufacture"
						and a.docstatus = 1
					"""
		query2 += """ and  c.item_name = '%s'  """ % q[0]
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

