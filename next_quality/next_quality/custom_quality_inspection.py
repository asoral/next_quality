from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.model.mapper import get_mapped_doc
from frappe import _
from frappe.utils import flt, cint
from nextquality.next_quality.custom_quality_inspection_template import get_template_details
from erpnext.stock.doctype.quality_inspection.quality_inspection import QualityInspection
import json

class CustomQualityInspection(QualityInspection):
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


    
def on_submit(self,method):
    count = 0
    for i in self.readings:
        if i.get('status') == "Rejected":
            count = count + 1
    if (count == 0):
        self.status = "Accepted"
    else:
        self.status = "Rejected"


def set_insepection_in_batch(qc,method):
    if qc.item_code:
        item_doc = frappe.get_doc("Item", qc.item_code)
        if item_doc.has_batch_no and not qc.batch_no:
            frappe.throw("Batch No. is required.")

    if qc.batch_no and qc.readings:
        batch = frappe.get_doc("Batch", qc.batch_no)
        batch.last_test_date = datetime.now()
        batch.last_quality_inspection = qc.name
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
                               "values","selection","numeric","alphanumeric","formula_based_criteria" "min_value", "max_value"
                                ],
                        filters={'parenttype': 'Quality Inspection Template', 'parent': quality_inspection_template},
                        order_by="idx")

def set_inps(self,method):
    if self.reference_type== "Work Order":
        doc=frappe.get_doc("Work Order",self.reference_name)
        for i in doc.get('quality_inspection_parameter'):
            i.inprocess_quality_inspection = self.name 
        doc.save(ignore_permissions=True)
    
    

@frappe.whitelist()
def get_parameter_values(quality_inspection_template_name):
    # doc=frappe.db.sql("""select i.values from `tabItem Quality Inspection Parameter` i,`tabQuality Inspection` q  where i.parent=q.quality_inspection_template """)
    print("************")
    doc = frappe.get_doc("Quality Inspection Template",quality_inspection_template_name)
    c=[]
    for i in doc.get('item_quality_inspection_parameter'):
        if not i.values:
            pass
        else:
            con_to_json = json.loads(i.get('values'))
            print(con_to_json)
            for a in con_to_json:
                b=a.get("value")
                c.append(b)
            return c



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
        if se_doc.stock_entry_type == "Manufacture":
            for line in se_doc.items:
                if line.is_finished_item:
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
        else:
            for line in se_doc.items:
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




