from __future__ import unicode_literals
import frappe
import json
import math
from frappe import _
from frappe.utils import flt, get_datetime, getdate, date_diff, cint, nowdate, get_link_to_form, time_diff_in_hours
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def create_quality_inspection(doc_name):
    doc = frappe.get_doc("Purchase Receipt",doc_name)
    for item in doc.items:
        itm_detail = frappe.db.get_all('Item', filters={'name': item.item_code},
                                  fields=["inspection_required_before_purchase","inspection_required_before_delivery",
                                          "quality_inspection_template"])



        for inspect_det in itm_detail:

            if doc.doctype == "Purchase Receipt" and inspect_det.inspection_required_before_purchase == 1:
                doc_qi = frappe.new_doc("Quality Inspection")
                ref_type = "In Process"
                if (doc.doctype == "Purchase Receipt" or doc.doctype == "Purchase Invoice"):
                    ref_type = "Incoming"
                if (doc.doctype == "Delivery Note" or doc.doctype == "Sales Invoice"):
                    ref_type = "Outgoing"
                doc_qi.inspection_type = ref_type
                doc_qi.reference_type = doc.doctype
                doc_qi.reference_name = doc.name
                doc_qi.item_code = item.item_code
                doc_qi.batch_no = item.batch_no
                doc_qi.sample_size = "1"
                doc_qi.inspected_by = frappe.session.user
                doc_qi.quality_inspection_template = inspect_det.quality_inspection_template
                if inspect_det.quality_inspection_template:
                    obj = frappe.get_doc("Quality Inspection Template",inspect_det.quality_inspection_template)
                    for ro in obj.item_quality_inspection_parameter:
                        doc_qi.append("readings", {
                            'specification': ro.specification,
                            'numeric': ro.numeric,
                            'selection':ro.selection,
                            'alphanumeric':ro.alphanumeric,
                            'values':ro.values,
                            'value':ro.value,
                            'formula_based_criteria': ro.formula_based_criteria,
                            'acceptance_formula': ro.acceptance_formula,
                            'min_value': ro.min_value,
                            'max_value': ro.max_value
                        })
                doc_qi.insert(ignore_permissions=True)
                # doc.submit()
                q = "update `tab{0} Item`  set quality_inspection_created = 1 where parent = '{1}' and item_code = '{2}';".format(
                    doc.doctype, doc.name, item.item_code)
                if (doc.doctype == "Stock Entry"):
                    q = "update `tabStock Entry Detail`  set quality_inspection_created = 1 where parent = '{0}' and item_code = '{1}';".format(
                        doc.name, item.item_code)
                frappe.db.sql(q)
                frappe.db.commit()
    return True


    def before_submit(self,method):
    doc=frappe.db.get_value("Quality Inspection",{"reference_name":self.name},["reference_name","item_code"],as_dict=1)
    if self.name == doc.get('reference_name'):
            pass
    else:
            msg="Quality Inspection Not found for item {0}".format(i.item_code)
            frappe.throw(msg)


    if doc.get('status') in ["Rejected","Not Tested"]:
            msg="Quality Inspection is Rejected or Not Tested"
            frappe.throw(msg)

    def before_save(self,method):
    #doc = frappe.db.sql("""SELECT item_code FROM `tabItem` WHERE has_batch_no = 1""", as_dict = True)
    all_doc = frappe.db.get_all("Item", {"has_batch_no" : 1}, ['item_code'])
    doc = []
    for d in all_doc:
        doc.append(d.get("item_code"))
    for i in self.items:
        print(i.item_code)
        if i.item_code in doc:
           frappe.throw("batch no required")
        else:
            pass