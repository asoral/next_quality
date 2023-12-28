from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


def before_insert(self,method):
	list=frappe.db.get_all("Quality Inspection Template",{"inspection_applicable_on":self.inspection_applicable_on,"bom":self.bom,"inspection_type":self.inspection_type}
			,["bom","inspection_applicable_on","inspection_type"])
	if list:
	    msg="There is already a Quality Inspection created for {0} with same Inspection Type and Applicability. Please edit that inspection or delete and recreate one.".format(self.bom)
	    frappe.throw(msg)
	
	
# def before_save(self,method):
# 	doc=frappe.get_doc("Quality Inspection Template",{"bom":self.select_intermediate_bom_to_copy_results_from})
# 	frappe.db.sql("delete from `tabQuality Inspection Template` where bom =%s", (self.select_intermediate_bom_to_copy_results_from))

# 	if self.select_intermediate_bom_to_copy_results_from==doc.bom:
# 		print(doc.bom)
# 	# doc_qi.quality_inspection_template = inspect_det.quality_inspection_template
# 		for res in doc.item_quality_inspection_parameter:
# 			r = res.as_dict()
# 			doc.append("item_quality_inspection_parameter", r)
# 		doc.flags.ignore_validate_update_after_submit = True
# 		doc.save(ignore_permissions=True)
# 		doc.clear_cache()
# 		doc.reload()
			

@frappe.whitelist()
def get_list():
	list=[]
	lst=frappe.db.get_all("Quality Inspection Template",{"inspection_type":"On Finish"},['bom'])
	for i in lst:
		list.append(i.get('bom'))
		print(list)
	return list

pass

def get_template_details(template):
	if not template: return []

	return frappe.get_all('Item Quality Inspection Parameter',
		fields=["specification", "value", "acceptance_formula",
			"numeric", "formula_based_criteria","selection","values", "min_value", "max_value","descriptions"],
		filters={'parenttype': 'Quality Inspection Template', 'parent': template},
		order_by="idx")



