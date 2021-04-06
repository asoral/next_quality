from __future__ import unicode_literals
import frappe
from frappe.model.mapper import get_mapped_doc


def set_inq(name):
	doc=frappe.db.get_all("InProcess Quality Inspection",{"reference_name":name},['name'])
	for i in doc:
		lst=i.get('name')
	return lst

@frappe.whitelist()
def create_inps_qlt_ins(doctype,name,production_item,template):
	res = []
	res = template.split(",")
	for temp in res:
		iqit_doc = frappe.new_doc("Quality Inspection")
		iqit_doc.inspection_type = "In Process"
		iqit_doc.reference_type = doctype
		iqit_doc.reference_name = name
		iqit_doc.item_code = production_item
		iqit_doc.sample_size = "1"
		iqit_doc.inspected_by = frappe.session.user
		iqit_doc.quality_inspection_template = temp
		obj = frappe.get_doc("Quality Inspection Template",temp)
		for row in obj.item_quality_inspection_parameter:
			iqit_doc.append("readings",{
				'specification': row.specification,
				'numeric': row.numeric,
				'value': row.value,
				'alphanumeric':row.alphanumeric,
				'values':row.values,
				'formula_based_criteria': row.formula_based_criteria,
				'acceptance_formula': row.acceptance_formula,
				'min_value': row.min_value,
				'max_value': row.max_value
			})
		iqit_doc.save(ignore_permissions=True)
	return True


@frappe.whitelist()
def get_inprocess_qit(bom):
	QIT = frappe.db.get_all("Quality Inspection Template", fields=["name","quality_inspection_template_name","inspection_type","inspection_applicable_on","periodicity"],
                            filters={ "inspection_applicable_on": "Work Order",
									 "bom":bom}, order_by="idx")
	return QIT

@frappe.whitelist()
def create_QIT(source_name, target_doc=None):
	doc = get_mapped_doc("Work Order", source_name, {
		"Work Order": {
			"doctype": "Quality Inspection",
			"validation": {
				"docstatus": ["=", 1]
			}
		}
	}, target_doc)

	return doc



def periodic_quality_inspection():
	WIQIT = frappe.db.get_all("Work InProcess Quality Inspection Template", fields=["parent", "parenttype",
																					"quality_inspection_template"],
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
		obj = frappe.get_doc("Quality Inspection Template", res.inprocess_quality_inspection_template)
		for row in obj.item_quality_inspection_parameter:
			iqit_doc.append("readings", {
				'specification': row.specification,
				'numeric': row.numeric,
				'value': row.value,
				'selection':row.selection,
				'values': row.values,
				'alphanumeric':row.alphanumeric,
				'formula_based_criteria': row.formula_based_criteria,
				'acceptance_formula': row.acceptance_formula,
				'min_value': row.min_value,
				'max_value': row.max_value
			})
		iqit_doc.save(ignore_permissions=True)
        