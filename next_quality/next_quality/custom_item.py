from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def show_inprocess_template():
    item=[]
    doc=frappe.db.sql("""select quality_inspection_template_name from `tabQuality Inspection Template` where inprocess_quality_inspection = 0""",as_dict=1)
    for i in doc:
        j=i.get("quality_inspection_template_name")
        item.append(j)
    return item