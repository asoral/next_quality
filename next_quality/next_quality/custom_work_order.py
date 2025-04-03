from __future__ import unicode_literals
import frappe
from frappe.model.mapper import get_mapped_doc

# @frappe.whitelist()
# def timelogs_data(self,method):
# 	job_cards = frappe.get_all("Job Card", filters={"work_order": self.name}, fields=["name", "expected_start_date", "expected_end_date", "for_quantity"])
# 	for job_card in job_cards:
# 		doc = frappe.get_doc("Job Card", job_card.name)
# 		doc.append("time_logs", {
# 			"from_time": job_card.get("expected_start_date"),
# 			"to_time": job_card.get("expected_end_date"),
# 			"completed_qty": job_card.get("for_quantity")
# 		})
# 	self.submit()

@frappe.whitelist()
def set_inq(name):
	doc=frappe.db.get_all("Quality Inspection",{"reference_name":name},['name'])
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
				'descriptions':row.descriptions,
				'numeric': row.numeric,
				'value': row.value,
				'values':row.values,
				'formula_based_criteria': row.formula_based_criteria,
				'acceptance_formula': row.acceptance_formula,
				'min_value': row.min_value,
				'max_value': row.max_value
			})
		iqit_doc.save(ignore_permissions=True)
	frappe.db.set_value(doctype, name, 'custom_quality_inspection_created', 1)
	frappe.msgprint("Quality Inspection Created")
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
				'value': row.value,
				'selection':row.selection,
				'values': row.values,
				'descriptions':row.descriptions,
				'formula_based_criteria': row.formula_based_criteria,
				'acceptance_formula': row.acceptance_formula,
				'min_value': row.min_value,
				'max_value': row.max_value
			})
		iqit_doc.save(ignore_permissions=True)
        

def validate_Qc(self,method):
	if self.bom_no:
		doc=frappe.db.get_value("Quality Inspection Template",{"bom":self.bom_no},["name"])
		if not doc:
			frappe.throw("Quality Inspection Template Not Found against Bom")
