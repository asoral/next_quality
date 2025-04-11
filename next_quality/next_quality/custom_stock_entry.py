from __future__ import unicode_literals
import frappe
from datetime import datetime

@frappe.whitelist()
def create_quality_inspection(doctype,name,work_order):
    work_order_data = frappe.get_doc("Work Order",work_order)
    inspection_type = None
    template = None
    for qua_insp in work_order_data.quality_inspection_parameter:
        inspection_type = qua_insp.inspection_type
        template = qua_insp.inprocess_quality_inspection_template

    st_doc = frappe.get_doc("Stock Entry",name)
    item_code = None
    batch_no = None
    for item in st_doc.items:
        item_code = item.item_code
        batch_no = item.batch_no
    
    iqit_doc = frappe.new_doc("Quality Inspection")
    iqit_doc.inspection_type = "In Process"
    iqit_doc.reference_type = "Work Order"
    iqit_doc.reference_name = work_order
    iqit_doc.custom_stock_entry = name
    iqit_doc.item_code = item_code
    iqit_doc.inps_type = inspection_type
    iqit_doc.batch_no = batch_no
    iqit_doc.sample_size = "1"
    iqit_doc.inspected_by = frappe.session.user
    iqit_doc.bom_no = st_doc.bom_no
    iqit_doc.quality_inspection_template = template
    obj = frappe.get_doc("Quality Inspection Template",template)
    for row in obj.item_quality_inspection_parameter:
        iqit_doc.append("readings",{
            'specification': row.specification,
            'descriptions':row.descriptions,
            'numeric': row.numeric,
            'value': row.value,
            'values':row.values,
            'formula_based_criteria': row.formula_based_criteria,
            'acceptance_formula': row.acceptance_formula,
            'min_value': row.min_value,
            'max_value': row.max_value
        })
    iqit_doc.save(ignore_permissions=True)
    frappe.db.set_value(doctype, name, 'custom_quality_inspection_created', 1)
    frappe.msgprint("Quality Inspection Created")
    return True


def delete_quality_inspection(self,method):
    if self.custom_stock_entry:
        stock_entry = frappe.get_doc("Stock Entry",self.custom_stock_entry)
        if stock_entry.custom_quality_inspection_created == 1 and stock_entry.stock_entry_type == "Manufacture":
            stock_entry.db_set("custom_quality_inspection_created", 0, update_modified = False)
            frappe.db.set_value("Stock Entry", stock_entry.name, 'custom_quality_inspection_created', 0)


def submit_quality_inspection(self,method):
    if self.custom_quality_inspection_created ==1 and self.stock_entry_type == "Manufacture":
        quality_insp = frappe.get_doc("Quality Inspection",{"custom_stock_entry":self.name})
        if quality_insp.docstatus != 1:
            frappe.throw("Please Submit the Quality Inspection.")
        else:
            quality_doc = frappe.get_doc("Stock Entry",{"name":self.name})
            batch_no = None
            for item in quality_doc.items:
                batch_no = item.batch_no
            frappe.db.set_value("Quality Inspection",quality_insp.name,"batch_no",batch_no)

    

def create_quality_insp(self,method):
    if self.custom_on_finish_inspection_required == 1 and self.docstatus != 1 and self.stock_entry_type == "Manufacture":
        frappe.frappe.msgprint('"Please Create On Finish Quality Inspection"')


@frappe.whitelist()
def get_list(company):
	list=[]
	lst=[]
	doc=frappe.db.get_all("Stock Entry",{"stock_entry_type":"Send to Subcontractor","docstatus":1,"company":["!=", company],'posting_date': ['>=', '2021-07-08']},['name'])

	db=frappe.db.get_all("Stock Entry",{"stock_entry_type":"Material Receipt","docstatus":1},['reference_challan'])
	for i in db:
		if i.reference_challan:
			lst.append(i.reference_challan)
	for i in doc:
		if i.name not in lst:
			list.append(i.name)
	return list


def on_submit(self,method):
    pass
    # if self.material_produce:
    #     lst = frappe.get_doc("Material Produce",self.material_produce)
    #     for i in lst.material_produce_item:
    #         if i.type=="FG":
    #             l=frappe.get_doc("Work Order",self.work_order)
    #             a=l.production_item
    #             for a in self.items:
    #                 batch_no = a.batch_no if self.docstatus == 1 else ""
    #                 if lst.quality_inspection_created==1:
    #                     doc = frappe.get_doc("Quality Inspection",lst.quality_inspection)
    #                     if doc.reference_type=="Work Order"and doc.inps_type=="On Finish":
    #                         if a.batch_no and lst.quality_inspection and a.batch_no!=doc.batch_no and a.item_code==doc.item_code:
    #                             q="""
    #                             UPDATE `tabQuality Inspection`
    #                             SET batch_no ='{0}', modified = '{1}'
    #                             WHERE name = '{2}' and item_code = '{3}'
    #                             """.format(a.batch_no, a.modified , lst.quality_inspection,doc.item_code)
    #                             frappe.db.sql(q)
    #                             frappe.db.commit()
    #                             doc.reload()
    #                         if doc.batch_no and doc.readings:
    #                             batch = frappe.get_doc("Batch", doc.batch_no)
    #                             batch.last_test_date = datetime.now()
    #                             # batch.last_quality_inspection = doc.name
    #                             batch.quality_inspection = lst.quality_inspection
    #                             frappe.db.sql("delete from `tabQuality Inspection Reading` where parent =%s", (batch.name))
    #                             for res in doc.readings:
    #                                 r = res.as_dict()
    #                                 r.pop("name")
    #                                 r.pop("owner")
    #                                 r.pop("creation")
    #                                 r.pop("modified")
    #                                 r.pop("modified_by")
    #                                 r.pop("parent")
    #                                 r.pop("parentfield")
    #                                 r.pop("parenttype")
    #                                 r.pop("idx")
    #                                 r.pop("docstatus")
    #                                 batch.append("test_result", r)
    #                             batch.flags.ignore_validate_update_after_submit = True
    #                             batch.save(ignore_permissions=True)
    #                             batch.clear_cache()
    #                             batch.reload()

    #                     else:
    #                         pass
    #                 else:
    #                     pass
           
    # else:
    #     pass
