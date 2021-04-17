from __future__ import unicode_literals
import frappe


# def on_submit(self,method):
#     doc=frappe.get_doc("Stock Entry",{"material_produce":self.name})
#     doc.quality_inspection=self.quality_inspection
#     doc.save(ignore_permissions=True)
#     doc.reload()

def before_submit(self,method):
    doc = frappe.get_doc("Work Order",self.work_order)
    if self.quality_inspection_created==1:
        doc = frappe.get_doc("Quality Inspection",{"reference_name":self.work_order})
        if doc.inps_type=="On Finish" and doc.reference_name==self.work_order and doc.status == "Not Tested" and doc.docstatus==0:
            frappe.throw("Please complete quality Inspection created on Work Order {0}".format(self.work_order))
        else:
            pass
    elif self.quality_inspection_created==0:
        doc = frappe.get_doc("Work Order",self.work_order)
        for row in doc.quality_inspection_parameter:
            if row.inspection_type=="On Finish":
                frappe.throw("Quality Inspection is applied for FG on BOM, please create a quality inspection before submitting the production details.")
            else:
                pass
    else:
        pass


        

@frappe.whitelist()
def create_inps(work_order):
    doc = frappe.get_doc("Work Order",work_order)
    print(doc)
    for row in doc.quality_inspection_parameter:
        if row.inspection_type=="On Finish":
            iqit_doc = frappe.new_doc("Quality Inspection")
            iqit_doc.inspection_type = "In Process"
            iqit_doc.reference_type = doc.doctype
            iqit_doc.reference_name = doc.name
            iqit_doc.item_code = doc.production_item
            iqit_doc.bom_no = doc.bom_no
            iqit_doc.sample_size = "1"
            iqit_doc.inspected_by = frappe.session.user
            iqit_doc.quality_inspection_template = row.inprocess_quality_inspection_template
            iqit_doc.inps_type=row.inspection_type
            obj = frappe.get_doc("Quality Inspection Template", row.inprocess_quality_inspection_template)
            for ro in obj.item_quality_inspection_parameter:
                iqit_doc.append("readings", {
                    'specification': ro.specification,
                    'numeric': ro.numeric,
                    'values': ro.values,
                    'value':ro.value,
                    'selection':ro.selection,
                    'formula_based_criteria': ro.formula_based_criteria,
                    'acceptance_formula': ro.acceptance_formula,
                    'min_value': ro.min_value,
                    'max_value': ro.max_value
                    })
            iqit_doc.insert(ignore_permissions=True)
    return True