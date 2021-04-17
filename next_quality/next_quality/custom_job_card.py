from __future__ import unicode_literals
import frappe
import json
import math
from frappe import _
from frappe.utils import flt, get_datetime, getdate, date_diff, cint, nowdate, get_link_to_form, time_diff_in_hours
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

def make_inprocess_quality_inspection(self,method):
	lst=frappe.db.get_value("Quality Inspection",{"reference_name":self.work_order},["reference_name"])
	if not lst:
		doc = frappe.get_doc("Work Order", self.work_order)
		for row in doc.quality_inspection_parameter:
			if row.inspection_type == "On Start" and doc.status == "In Process":
				iqit_doc = frappe.new_doc("Quality Inspection")
				iqit_doc.inspection_type = "In Process"
				iqit_doc.reference_type = doc.doctype
				iqit_doc.reference_name = doc.name
				iqit_doc.item_code = doc.production_item
				iqit_doc.sample_size = "1"
				iqit_doc.inspected_by = frappe.session.user
				iqit_doc.quality_inspection_template = row.inprocess_quality_inspection_template
				iqit_doc.inps_type=row.inspection_type
				obj = frappe.get_doc("Quality Inspection Template", row.inprocess_quality_inspection_template)
				for ro in obj.item_quality_inspection_parameter:
					iqit_doc.append("readings", {
						'specification': ro.specification,
						'numeric': ro.numeric,
						'value': ro.value,
						'selection':ro.selection,
						'values': ro.values,
						'formula_based_criteria': ro.formula_based_criteria,
						'acceptance_formula': ro.acceptance_formula,
						'min_value': ro.min_value,
						'max_value': ro.max_value
					})
				iqit_doc.save(ignore_permissions=True)

@frappe.whitelist()
def get_inprocess_qite(bom,workstation):
    QIT = frappe.db.get_all("Quality Inspection Template", fields=["name","quality_inspection_template_name","inspection_type","inspection_applicable_on","periodicity"],
                            filters={ "inspection_applicable_on": "Job Card",
									 "bom":bom,"workstation_":workstation}, order_by="idx")

    return QIT

def periodic_quality_inspect():
	WIQIT = frappe.db.get_all("Work InProcess Quality Inspection Template", fields=["parent", "parenttype",
																					"quality_inspection_template","inspection_type"],
							filters={ "docstatus": 1,'inspection_type':'Periodic'})
	for res in WIQIT:
		obj = frappe.get_doc("Quality Inspection Template", res.inprocess_quality_inspection_template)
		hrs = obj.periodicity
		obj = frappe.get_doc(res.parenttype,res.parent)
		iqit_doc = frappe.new_doc("Quality Inspection")
		iqit_doc.inspection_type = "In Process"
		iqit_doc.reference_type = res.parenttype
		iqit_doc.reference_name = res.parent
		iqit_doc.item_code = obj.production_item
		iqit_doc.sample_size = "1"
		iqit_doc.inspected_by = frappe.session.user
		iqit_doc.inps_type=res.inspection_type
		obj = frappe.get_doc("Quality Inspection Template", res.inprocess_quality_inspection_template)
		for row in obj.item_quality_inspection_parameter:
			iqit_doc.append("readings", {
				'specification': row.specification,
				'numeric': row.numeric,
				'value':row.value,
				'values': row.values,
				'selection':row.selection,
				'formula_based_criteria': row.formula_based_criteria,
				'acceptance_formula': row.acceptance_formula,
				'min_value': row.min_value,
				'max_value': row.max_value
			})
		iqit_doc.save(ignore_permissions=True)