from __future__ import unicode_literals
import frappe
from frappe import _
import json
from frappe.utils import flt, cint

def get_list(self,method):
    for i in self.items:
        a=[]
        a.append(i.against_sales_order)
        b=i.batch_no
        count=frappe.db.sql("""select distinct count(qci.name) as count from `tabCustomer Quality Inspection` qci where qci.sales_order='{0}' and qci.item='{1}'and qci.docstatus=1""".format(i.against_sales_order,i.item_code),as_dict=1)
        for j in count:
            if j.get('count')>0:
                doc=frappe.get_doc("Customer Quality Inspection",{"sales_order":i.against_sales_order,"docstatus":1})
                print(doc.name)
                if doc.item==i.item_code:
                    lst=frappe.get_doc("Batch",b)
                    for row1 in doc.item_quality_inspection_parameter:
                        if row1.specification:
                            for row2 in lst.test_result:
                                if row1.specification == row2.specification:
                                    if not row2.reading_1 and row1.numeric==1:
                                        frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")
                                    elif row2.reading_1 and row1.numeric==1 and row2.numeric==1 and row1.formula_based_criteria==0 and row2.formula_based_criteria==0:
                                        if float(row2.reading_1) <= row1.min_value or float(row2.reading_1) >= row1.max_value:
                                            frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")

                                elif row1.specification == row2.specification:
                                    if not row2.reading_value and row1.numeric==0 and row1.formula_based_criteria==0 and row1.selection==0:
                                        frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement$")
                                    elif row2.reading_value and row1.value!=row2.reading_value:
                                        if row1.numeric==row2.numeric and row1.formula_based_criteria==row2.formula_based_criteria and row1.selection==row2.selection:
                                            frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")
                                    else:
                                        pass
                                
                                elif row1.specification == row2.specification :
                                    if not row2.parameter_value and row1.selection==1:
                                        frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")
                                    elif row2.parameter_value and row1.selection==1 and row2.selection==1:
                                        print(row1.get('values'))
                                        con_to_json = json.loads(row1.get('values'))
                                        b=[]
                                        for a in con_to_json:
                                            b.append(a.get('value'))
                                        if row2.parameter_value not in b:
                                            frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")
                                elif row1.specification == row2.specification :
                                    if not row2.reading_1 and row1.numeric==1 and row1.formula_based_criteria==1 :
                                        frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")
                                    elif row2.reading_1 and row1.numeric==1 and row2.numeric==1 and row1.formula_based_criteria==1 and row2.formula_based_criteria==1:
                                        from statistics import mean
                                        readings_list = []
                                        for i in range(1, 11):
                                            reading_value = row2.get("reading_" + str(i))
                                            if reading_value is not None and reading_value.strip():
                                                readings_list.append(flt(reading_value))

                                            actual_mean = mean(readings_list) if readings_list else 0
                                        data = {}
                                        for i in range(1, 11):
                                            field = "reading_" + str(i)
                                            data[field] = flt(row2.get(field))
                                        data["mean"] = actual_mean
                                        condition=row1.acceptance_formula 
                                        result = frappe.safe_eval(condition, None, data)
                                        print(result)
                                        if result :
                                            pass
                                        else:
                                            frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")
                                elif row1.specification == row2.specification:
                                    if not row2.reading_value and row1.numeric==0 and row1.formula_based_criteria==1:
                                        frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")
                                    elif row2.reading_value and row1.numeric==0 and row2.numeric==0 and row1.formula_based_criteria==1 and row2.formula_based_criteria==1:
                                        data = {"reading_value": row2.get("reading_value")}
                                        condition=row1.acceptance_formula 
                                        result = frappe.safe_eval(condition, None, data)
                                        print(result)
                                        if result :
                                            pass
                                        else:
                                            frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")
                                else:
                                    frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")

                        else:
                            pass
                else:
                    pass
            