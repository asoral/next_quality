from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.model.mapper import get_mapped_doc
from frappe import _
from frappe.utils import flt, cint
from next_quality.next_quality.custom_quality_inspection_template import get_template_details
from erpnext.stock.doctype.quality_inspection.quality_inspection import QualityInspection
import json

class CustomQualityInspection(QualityInspection):
    @frappe.whitelist()
    def get_item_specification_details(self):
        if not self.quality_inspection_template:
            self.quality_inspection_template = frappe.db.get_value('Item',
                self.item_code, 'quality_inspection_template')

        if not self.quality_inspection_template: return

        self.set('readings', [])
        parameters = get_template_details(self.quality_inspection_template)
        for d in parameters:
            child = self.append('readings', {})
            child.update(d)
            child.status = "Accepted"

    def update_qc_reference(self):
        quality_inspection = self.name if self.docstatus == 1 else ""

        if self.reference_type == 'Job Card':
            if self.reference_name:
                frappe.db.sql("""
                    UPDATE `tab{doctype}`
                    SET quality_inspection = %s, modified = %s
                    WHERE name = %s and production_item = %s
                """.format(doctype=self.reference_type),
                    (quality_inspection, self.modified, self.reference_name, self.item_code))
        elif self.reference_type == 'Work Order':
            if self.reference_name:
                frappe.db.sql("""
					UPDATE `tab{doctype}`
					SET quality_inspection = %s, modified = %s
					WHERE name = %s and production_item = %s
				    """.format(doctype=self.reference_type),
					(quality_inspection, self.modified, self.reference_name, self.item_code))

        else:
            args = [quality_inspection, self.modified, self.reference_name, self.item_code]
            doctype = self.reference_type + ' Item'

            if self.reference_type == 'Stock Entry':
                doctype = 'Stock Entry Detail'

            if self.reference_type and self.reference_name:
                conditions = ""
                if self.batch_no and self.docstatus == 1:
                    conditions += " and t1.batch_no = %s"
                    args.append(self.batch_no)

                if self.docstatus == 2: # if cancel, then remove qi link wherever same name
                    conditions += " and t1.quality_inspection = %s"
                    args.append(self.name)

                    frappe.db.sql("""
					UPDATE
						`tab{child_doc}` t1, `tab{parent_doc}` t2
					SET
						t1.quality_inspection = %s, t2.modified = %s
					WHERE
						t1.parent = %s
						and t1.item_code = %s
						and t1.parent = t2.name
						{conditions}
				    """.format(parent_doc=self.reference_type, child_doc=doctype, conditions=conditions),
					args)
  
def before_save(self,method):
    count = 0
    null =0
    for i in self.readings:
        if i.numeric == 1 :
            if not i.get("reading_1"):
                null=null+1
        if i.numeric == 0 and i.formula_based_criteria ==0 and i.selection==0:
            if not i.get("reading_value"):
                null=null+1
        if i.selection == 1:
            if not i.get("parameter_value"):
               null=null+1
        if i.status == "Rejected":
            count = count + 1
    if count == 0 and null == 0 :
        self.status = "Accepted"
        self.not_tested = 0
    if count > 0 :
        print(count)
        self.status ="Rejected"
        self.not_tested = 0
    if null > 0:
        self.not_tested = 1



def before_submit(self,method):
    if self.not_tested == 1:
        frappe.throw("Quality Inspection has not been completed. The status for document has to be Accepted or Rejected before you can post it.")
    else:
        pass


def set_insepection_in_batch(qc,method):
    if qc.inps_type== "On Finish":
        doc=frappe.get_doc("Material Produce",{"work_order":qc.reference_name})
        doc.quality_inspection=qc.name
        doc.save(ignore_permissions=True)
        doc.reload()

    if qc.batch_no:
        if qc.reference_type== "Purchase Receipt":
            doc=frappe.get_doc("Purchase Receipt",qc.reference_name)
            for i in doc.get('items'):
                i.batch_no = qc.batch_no
            doc.save(ignore_permissions=True)
            doc.reload()
        else:
            pass

    if qc.batch_no and qc.readings:
        batch = frappe.get_doc("Batch", qc.batch_no)
        # batch.last_test_date = datetime.now()
        # batch.last_quality_inspection = qc.name
        # batch.quality_inspection = qc.name
        batch.reference_doctype=qc.reference_type
        batch.reference_name=qc.reference_name
        frappe.db.sql("delete from `tabQuality Inspection Reading` where parent =%s", (batch.name))
        for res in qc.readings:
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
    

def set_batch_no(self):
    doc = frappe.get_doc("Stock Entry", self.item_code)
    for i in doc.get("items"):
        if not i.batch_no:
            pass
        else:
            self.batch_no=i.batch_no
    doc.save(ignore_permissions=True)
        
@frappe.whitelist()
def get_item_specification_details(quality_inspection_template,item_code = None):
    if not quality_inspection_template:
        if item_code != None:
            quality_inspection_template = frappe.db.get_value('Item',
                                                               item_code, 'quality_inspection_template')

    if not quality_inspection_template: return
    return frappe.get_all('Item Quality Inspection Parameter',
                        fields=[
                                "specification", "value", "acceptance_formula",
                               "values","selection","numeric","formula_based_criteria","min_value", "max_value","descriptions"
                                ],
                        filters={'parenttype': 'Quality Inspection Template', 'parent': quality_inspection_template},
                        order_by="idx")

def set_qc(self,method):
    if self.reference_type== "Purchase Receipt":
        doc=frappe.get_doc("Purchase Receipt",self.reference_name)
        for i in doc.get('items'):
            i.quality_inspection = self.name
        doc.save(ignore_permissions=True)
        doc.reload()

def set_inps(self,method):
    if self.reference_type== "Work Order":
        doc=frappe.get_doc("Work Order",self.reference_name)
        for i in doc.get('quality_inspection_parameter'):
            i.inprocess_quality_inspection = self.name
            i.reload() 
        doc.save(ignore_permissions=True)
        doc.reload()
    for i in self.readings:
        if i.parameter_value:
            doc = frappe.get_doc("Quality Inspection Template",self.quality_inspection_template)
            for j in doc.item_quality_inspection_parameter:
                if j.selection==1:
                    con_to_json = json.loads(j.get('values'))
                    if i.selection==1:
                        for a in con_to_json:
                            if a.get('value') == i.parameter_value and a.get('is_correct')==1:
                                i.status="Accepted"
                                break
                            elif a.get('value') == i.parameter_value and a.get('is_correct')==0:
                                i.status="Rejected"
                                break
    
                           
# @frappe.whitelist()
# def get_parameter_values(quality_inspection_template,name):
#     doc = frappe.get_doc("Quality Inspection Template",quality_inspection_template)
#     lst=frappe.get_doc("Quality Inspection",name)
#     c=[]
#     for i in doc.get('item_quality_inspection_parameter'):
#         for j in lst.readings:
#             # print("*********",j.specification)
#             # print("&&&&&",i.specification)
#             if not i.values:
#                 break
#             else:
#                 if i.specification==j.specification:
#                     con_to_json = json.loads(i.values)
#                     print(con_to_json)
#                     for a in con_to_json:
#                         # print(a)
#                         b=a.get("value")
#                         # print(b)
#                         c.append(b)
#     return c


@frappe.whitelist()
def make_quality_inspection(doc_name):
    sale_ord = frappe.get_doc("Sales Order",doc_name)
    if sale_ord:
        new_d = frappe.new_doc("Customer Quality Inspection")
        new_d.date = datetime.now().date()
        new_d.sales_order = sale_ord.name
        new_d.customer = sale_ord.customer
        new_d.customer_name = sale_ord.customer_name
        return new_d.as_dict()
    return False

@frappe.whitelist()
def make_quality_criteria(doc_name):
    customer = frappe.get_doc("Customer", doc_name)
    if customer:
        new_d = frappe.new_doc("Customer Inspection Criteria")
        new_d.customer = customer.name
        new_d.customer_name = customer.customer_name
        return new_d.as_dict()
    return False

@frappe.whitelist()
def make_stock_quality_inspec(doc_name, doctype):
    if doctype == "Stock Entry":
        se_doc = frappe.get_doc("Stock Entry", doc_name)
        if se_doc.stock_entry_type == "Repack":
            for line in se_doc.items:
                if line.is_finished_item==1:
                    item_doc = frappe.get_doc("Item",line.item_code)
                    doc = frappe.new_doc("Quality Inspection")
                    doc.inspection_type = "In Process"
                    doc.reference_type = doctype
                    doc.reference_name = se_doc.name
                    doc.item_code = line.item_code
                    doc.batch_no = line.batch_no
                    doc.sample_size = 1
                    doc.inspected_by = frappe.session.user
                    doc.quality_inspection_template = item_doc.quality_inspection_template
                    doc.insert(ignore_permissions=True)
        # else:
        #     for line in se_doc.items:
        #         item_doc = frappe.get_doc("Item",line.item_code)
        #         doc = frappe.new_doc("Quality Inspection")
        #         doc.inspection_type = "In Process"
        #         doc.reference_type = doctype
        #         doc.reference_name = se_doc.name
        #         doc.item_code = line.item_code
        #         doc.batch_no = line.batch_no
        #         doc.sample_size = 1
        #         doc.inspected_by = frappe.session.user
        #         doc.quality_inspection_template = item_doc.quality_inspection_template
        #         doc.insert(ignore_permissions=True)

    if doctype == "Delivery Note":
        dl_doc = frappe.get_doc("Delivery Note", doc_name)
        for line in dl_doc.items:
            item_doc = frappe.get_doc("Item", line.item_code)
            if item_doc.inspection_required_before_delivery:
                doc = frappe.new_doc("Quality Inspection")
                doc.inspection_type = "In Process"
                doc.reference_type = doctype
                doc.reference_name = dl_doc.name
                doc.item_code = line.item_code
                doc.batch_no = line.batch_no
                doc.sample_size = 1
                doc.inspected_by = frappe.session.user
                doc.quality_inspection_template = item_doc.quality_inspection_template
                doc.insert(ignore_permissions=True)
    return True




