# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class QualityInspectionCreationTool(Document):

	def make_quality_inspection(self):
		for row in self.inspections_to_be_created:
			itm = frappe.get_doc("Item",row.item)
			if itm.has_batch_no == 1 and not row.batch_no:
				frappe.throw(_("Batch Number Is Mandatory For Item : {0}").format(row.item))
			if itm.has_serial_no == 1 and not row.serial_no:
				frappe.throw(_("Serial Number Is Mandatory For Item : {0}").format(row.item))

		if(len(self.inspections_to_be_created) == 0):
			frappe.throw("Please select item first")
		for item in self.inspections_to_be_created:
			doc = frappe.new_doc("Quality Inspection")
			ref_type = "In Process"
			if(item.reference_doc == "Purchase Receipt" or item.reference_doc == "Purchase Invoice"):
				ref_type = "Incoming"
			if(item.reference_doc == "Delivery Note" or item.reference_doc == "Sales Invoice"):
				ref_type = "Outgoing"
			doc.inspection_type = ref_type
			doc.reference_type =  item.get("reference_doc")
			doc.reference_name = item.get("reference_name")
			doc.item_code = item.get("item")
			doc.batch_no = item.get("batch_no")
			doc.sample_size = item.get("sample_size")
			doc.inspected_by = frappe.session.user
			doc.quality_inspection_template = item.quality_inspection_template
			doc.insert(ignore_permissions=True)
			# doc.submit()
			q = "update `tab{0} Item`  set quality_inspection_created = 1 where parent = '{1}' and item_code = '{2}';".format(item.get("reference_doc"),item.get("reference_name"),item.get("item"))
			if(item.get("reference_doc") == "Stock Entry"):
				q = "update `tabStock Entry Detail`  set quality_inspection_created = 1 where parent = '{0}' and item_code = '{1}';".format(item.get("reference_name"),item.get("item"))
			frappe.db.sql(q)
			frappe.db.commit()
		return True
	
	def get_item_from_doc(self, doc):
		item_list = []
		get_item = frappe.get_all(doc, filters={"docStatus":"0","quality_inspection_created":"0" }, fields=["item_code","description", "serial_no","batch_no","parent"])
		if(doc == "Purchase Invoice Item"):
			item_list.clear()
			for item in get_item:
				item_to_be_inspected = frappe.db.get_value("Item", {"item_code":item.item_code,"inspection_required_before_purchase":"1"},["item_code","quality_inspection_template"])
				if(item_to_be_inspected):
					supplier_name= frappe.db.get_value("Purchase Invoice", {"name": item.parent}, ["supplier"])
					item.supplier = supplier_name
					item.template = item_to_be_inspected[1]
					item_list.append(item)
		if(doc == "Purchase Receipt Item"):
			item_list.clear()
			for item in get_item:
				item_to_be_inspected = frappe.db.get_value("Item", {"item_code":item.item_code,"inspection_required_before_purchase":"1"},["item_code","quality_inspection_template"])
				if(item_to_be_inspected):
					get_supplier_name = frappe.db.get_value("Purchase Receipt", {"name": item.parent}, ["supplier"])
					get_warehouse = frappe.db.get_value(doc, {"parent": item.parent}, ["warehouse"])
					item.destination_warehouse = get_warehouse
					item.supplier = get_supplier_name
					item.template = item_to_be_inspected[1]
					item_list.append(item)
		if(doc == "Delivery Note Item"):
			item_list.clear()
			for item in get_item:
				item_to_be_inspected = frappe.db.get_value("Item", {"item_code":item.item_code,"inspection_required_before_delivery":"1"},["item_code","quality_inspection_template"])
				if(item_to_be_inspected):
					get_customer_name = frappe.db.get_value("Delivery Note", {"name": item.parent}, ["customer"])
					get_warehouse = frappe.db.get_value(doc, {"parent": item.parent}, ["warehouse"])
					item.customer = get_customer_name
					item.source_warehouse = get_warehouse
					item.template = item_to_be_inspected[1]
					item_list.append(item)
		if(doc == "Sales Invoice Item"):
			item_list.clear()
			for item in get_item:
				item_to_be_inspected = frappe.db.get_value("Item", {"item_code":item.item_code,"inspection_required_before_delivery":"1"},["item_code","quality_inspection_template"])
				if(item_to_be_inspected):
					get_customer_name = frappe.db.get_value("Sales Invoice", {"name": item.parent}, ["customer"])
					get_warehouse = frappe.db.get_value(doc, {"parent": item.parent}, ["warehouse"])
					item.customer = get_customer_name
					item.source_warehouse = get_warehouse
					item.template = item_to_be_inspected[1]
					item_list.append(item)
		if(doc == "Stock Entry Detail"):
			item_list.clear()
			get_all_item = frappe.get_all(doc, filters={"docStatus":"0", "quality_inspection_created":"0"}, fields=["item_code","description", "serial_no","batch_no","parent", "t_warehouse"])
			for item in get_all_item:
				se_info = frappe.db.get_value("Stock Entry", {"name":item.parent},["stock_entry_type", "bom_no"])
				is_inspection_req = frappe.db.get_value("BOM", {"name":se_info[1]},["inspection_required","quality_inspection_template"])

				if(se_info[0] == "Material Transfer for Manufacture" and is_inspection_req[0] == 1):
					item_to_be_inspected = frappe.db.get_value("BOM Item", {"parent":se_info[1]},["item_code","qty"])
					item.qty = item_to_be_inspected[1]
					item.template = is_inspection_req[1]
					item.destination_warehouse = item.get("t_warehouse")
					item_list.append(item)
		return item_list
		