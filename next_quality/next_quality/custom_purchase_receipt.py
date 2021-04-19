from __future__ import unicode_literals
import frappe
import json
import math
from frappe import _
from frappe.utils import flt, get_datetime, getdate, date_diff, cint, nowdate, get_link_to_form, time_diff_in_hours
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from datetime import datetime


def on_submit(self,method):
    for i in self.items:
	if i.quality_inspection_created==1:
       		batch_no = i.batch_no if self.docstatus == 1 else "" 
        	doc = frappe.get_doc("Quality Inspection",i.quality_inspection)
        	if doc.reference_type=="Purchase Receipt":
            		if i.batch_no and i.quality_inspection and i.batch_no!=doc.batch_no:
                		q="""
					UPDATE `tabQuality Inspection`
					SET batch_no ='{0}', modified = '{1}'
					WHERE name = '{2}' and item_code = '{3}'
				    """.format(i.get('batch_no'), i.modified , i.quality_inspection, i.item_code)
                		frappe.db.sql(q)
                		frappe.db.commit()
                		doc.reload()
            	if doc.batch_no and doc.readings:
			batch = frappe.get_doc("Batch", doc.batch_no)
			batch.last_test_date = datetime.now()
			# batch.last_quality_inspection = doc.name
			batch.quality_inspection = i.quality_inspection
			frappe.db.sql("delete from `tabQuality Inspection Reading` where parent =%s", (batch.name))
			for res in doc.readings:
			    r = res.as_dict()
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
			    batch.append("test_result", r)
			batch.flags.ignore_validate_update_after_submit = True
			batch.save(ignore_permissions=True)
			batch.clear_cache()
			batch.reload()

		else:
		    pass

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
                doc_qi.status="Not Tested"
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



    
    




    
    
