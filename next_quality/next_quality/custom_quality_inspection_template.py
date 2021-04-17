from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


def before_insert(self,method):
	list=frappe.db.get_all("Quality Inspection Template",{"inspection_applicable_on":self.inspection_applicable_on,"bom":self.bom,"inspection_type":self.inspection_type}
			,["bom","inspection_applicable_on","inspection_type"])
	if list:
	    msg="There is already a Quality Inspection created for {0} with same Inspection Type and Applicability. Please edit that inspection or delete and recreate one.".format(self.bom)
	    frappe.throw(msg)

@frappe.whitelist()
def get_list(bom):
	list=[]
	list=frappe.db.get_all("Quality Inspection",{"inps_type":"On Finish","bom_no":bom},['bom_no'])
	for i in list:
		list.append(i.get('bom_no'))
		print(list)
	return list


def get_template_details(template):
	if not template: return []

	return frappe.get_all('Item Quality Inspection Parameter',
		fields=["specification", "value", "acceptance_formula",
			"numeric", "formula_based_criteria","selection","values", "min_value", "max_value"],
		filters={'parenttype': 'Quality Inspection Template', 'parent': template},
		order_by="idx")



