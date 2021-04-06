from __future__ import unicode_literals
import frappe

def before_submit(self,method):
        doc = frappe.get_doc("Work Order",self.work_order)
        for row in doc.quality_inspection_parameter:
            iqit_doc = frappe.new_doc("Quality Inspection")
            iqit_doc.inspection_type = "In Process"
            iqit_doc.reference_type = doc.doctype
            iqit_doc.reference_name = doc.name
            iqit_doc.item_code = doc.production_item
            iqit_doc.sample_size = "1"
            iqit_doc.inspected_by = frappe.session.user
            iqit_doc.quality_inspection_template = row.inprocess_quality_inspection_template
            obj = frappe.get_doc("Quality Inspection Template", row.inprocess_quality_inspection_template)
            for ro in obj.item_quality_inspection_parameter:
                iqit_doc.append("readings", {
                    'specification': ro.specification,
                    'numeric': ro.numeric,
                    'values': ro.values,
                    'alphanumeric':ro.alphanumeric,
                    'value':ro.value,
                    'selection':ro.selection,
                    'formula_based_criteria': ro.formula_based_criteria,
                    'acceptance_formula': ro.acceptance_formula,
                    'min_value': ro.min_value,
                    'max_value': ro.max_value
                    })
            iqit_doc.insert(ignore_permissions=True)