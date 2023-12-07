from __future__ import unicode_literals
import frappe



def before_submit(self,method):
    doc = frappe.get_doc("Work Order",self.work_order)
    if self.quality_inspection_created==1:
        lst=frappe.db.get_value("Quality Inspection",{"reference_name":self.work_order},['name'])
        if lst:
            doc = frappe.get_doc("Quality Inspection",{"reference_name":self.work_order})
            if doc.docstatus==0:
                frappe.throw("Please complete quality Inspection created on Work Order {0}".format(self.work_order))
            else:
                pass
    else:
        for i in self.material_produce_item:
            if i.qty_produced>0 and i.type=='FG':
                doc = frappe.get_doc("Work Order",self.work_order)
                for row in doc.quality_inspection_parameter:
                    if row.inspection_type=="On Finish":
                        frappe.throw("Quality Inspection is applied for FG on BOM, please create a quality inspection before submitting the production details.")
                    else:
                        pass
#quality Inspection
@frappe.whitelist()
def create_inps(work_order,name):
    doc=frappe.get_doc("Material Produce",name)
    for i in doc.material_produce_item:
        print(i.type)
        if i.type=="FG":
            doc = frappe.get_doc("Work Order",work_order)
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
                            'descriptions':ro.descriptions,
                            'selection':ro.selection,
                            'formula_based_criteria': ro.formula_based_criteria,
                            'acceptance_formula': ro.acceptance_formula,
                            'min_value': ro.min_value,
                            'max_value': ro.max_value
                            })
                    iqit_doc.insert(ignore_permissions=True)
                    return iqit_doc.name
            return True
        else:
            pass


#copy Quality Inspection
@frappe.whitelist()
def copy_inps(work_order,bom,item_name,name):
    doc=frappe.get_doc("Material Produce",name)
    for i in doc.material_produce_item:
        if i.type=="FG":
            doc = frappe.get_doc("Work Order",work_order)
            lst = frappe.get_doc("Quality Inspection Template",{"bom":bom})
            # l=frappe.db.get_value("Quality Inspection Template",{"bom":lst.select_intermediate_bom_to_copy_results_from},['name'],as_dict=True)
            bom = frappe.get_doc("BOM",{"name":lst.select_intermediate_bom_to_copy_results_from},["item_code"])
            
            if lst.inspection_type=="On Finish" and lst.inspection_applicable_on=="Work Order":
                iqit_doc = frappe.new_doc("Quality Inspection")
                iqit_doc.inspection_type = "In Process"
                iqit_doc.reference_type = doc.doctype
                iqit_doc.reference_name = doc.name
                iqit_doc.item_code = doc.production_item
                iqit_doc.bom_no = doc.bom_no
                iqit_doc.sample_size = "1"
                iqit_doc.inspected_by = frappe.session.user
                # iqit_doc.quality_inspection_template = l.get('name')
                iqit_doc.inps_type=lst.inspection_type
                obj=frappe.get_doc("Quality Inspection",{"bom_no":lst.select_intermediate_bom_to_copy_results_from})
                print(obj.status)
                if obj.status=="Accepted" and obj.inps_type=="On Finish" and obj.readings:
                    for ro in obj.readings:
                        r = ro.as_dict()
                        r.pop("name")
                        r.pop("owner")
                        r.pop("creation")
                        r.pop("modified")
                        r.pop("modified_by")
                        r.pop("parent")
                        r.pop("parentfield")
                        r.pop("parenttype")
                        r.pop("idx")
                        r.pop("docstatus")
                        iqit_doc.append("readings", r)
                    iqit_doc.flags.ignore_validate_update_after_submit = True
                    iqit_doc.save(ignore_permissions=True)
                    iqit_doc.clear_cache()
                    iqit_doc.reload()
            iqit_doc.save(ignore_permissions=True)
            iqit_doc.submit()
            return iqit_doc.name
        else:
            pass
    
