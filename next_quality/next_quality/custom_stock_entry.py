from __future__ import unicode_literals
import frappe
from datetime import datetime


def on_submit(self,method):
    if self.material_produce:
        lst = frappe.get_doc("Material Produce",self.material_produce)
        doc=frappe.get_doc("Work Order",self.work_order)
        a=doc.production_item
        for a in self.items:
            batch_no = a.batch_no if self.docstatus == 1 else ""
            if lst.quality_inspection:
                doc = frappe.get_doc("Quality Inspection",lst.quality_inspection)
                if doc.reference_type=="Work Order"and doc.inps_type=="On Finish":
                    if a.batch_no and lst.quality_inspection and a.batch_no!=doc.batch_no:
                        q="""
                        UPDATE `tabQuality Inspection`
                        SET batch_no ='{0}', modified = '{1}'
                        WHERE name = '{2}' and item_code = '{3}'
                        """.format(a.batch_no, a.modified , lst.quality_inspection, doc.item_code)
                        frappe.db.sql(q)
                        frappe.db.commit()
                        doc.reload()
                    if doc.batch_no and doc.readings:
                        batch = frappe.get_doc("Batch", doc.batch_no)
                        batch.last_test_date = datetime.now()
                        # batch.last_quality_inspection = doc.name
                        batch.quality_inspection = lst.quality_inspection
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
            else:
                pass
           
    else:
        pass
