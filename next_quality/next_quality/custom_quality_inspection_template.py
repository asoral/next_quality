import frappe
from frappe.model.document import Document


def before_insert(self,method):
	list=frappe.db.get_all("Quality Inspection Template",{"inspection_applicable_on":self.inspection_applicable_on,"bom":self.bom,"inspection_type":self.inspection_type,"mfg_inspection":1}
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

	fields = ["*", "specification", "value", "acceptance_formula",
			"numeric", "formula_based_criteria","selection","values", "min_value", "max_value","descriptions"]
	
	meta = frappe.get_meta('Item Quality Inspection Parameter')
	if meta.has_field('custom_coa_print_'):
		fields.append('custom_coa_print_')
	elif meta.has_field('coa_print'):
		fields.append('coa_print as custom_coa_print_')

	res = frappe.get_all('Item Quality Inspection Parameter',
		fields=["*"], # Fetch everything
		filters={'parenttype': 'Quality Inspection Template', 'parent': template},
		order_by="idx")

	# Universal mapping and data fixing
	for row in res:
		coa_print_val = ""
		if frappe.db.has_column("Item Quality Inspection Parameter", "custom_coa_print"):
			coa_print_val = frappe.db.get_value("Item Quality Inspection Parameter", row.name, "custom_coa_print")
		elif frappe.db.has_column("Item Quality Inspection Parameter", "custom_coa_print_"):
			coa_print_val = frappe.db.get_value("Item Quality Inspection Parameter", row.name, "custom_coa_print_")
		elif frappe.db.has_column("Item Quality Inspection Parameter", "coa_print"):
			coa_print_val = frappe.db.get_value("Item Quality Inspection Parameter", row.name, "coa_print")
		
		coa_print_val = coa_print_val or getattr(row, "custom_coa_print", None) or getattr(row, "custom_coa_print_", None) or getattr(row, "coa_print", None) or ""
		
		# Ensure it maps to both standard names for UI visibility
		row['custom_coa_print_'] = coa_print_val
		row['coa_print'] = coa_print_val
		
		if not row.get('status'):
			row['status'] = "Accepted"
			
	return res



