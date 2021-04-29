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
        doc=frappe.get_doc("Customer Quality Inspection",{"sales_order":a[0]})
        if doc.item==i.item_code:
            lst=frappe.get_doc("Batch",b)
            for row1 in doc.item_quality_inspection_parameter:
                if row1.specification:
                    for row2 in lst.test_result:
                        if row1.specification == row2.specification and row1.numeric and row1.formula_based_criteria==0 :
                            if float(row2.reading_1) <= row1.min_value or float(row2.reading_1) >= row1.max_value:
                                frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement ")
                        if row1.specification == row2.specification and row1.selection==0 and row1.numeric==0 and row1.formula_based_criteria==0:
                            if not row1.value==row2.reading_value:
                                frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")
                        if row1.specification == row2.specification and row1.selection:
                            con_to_json = json.loads(row1.get('values'))
                            for a in con_to_json:
                                print(a.get('value'))
                                print(row2.parameter_value)
                                if a.get('value') != row2.parameter_value:
                                    frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")
                        if row1.specification == row2.specification and row1.numeric and row1.formula_based_criteria:
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
                        if row1.specification == row2.specification and row1.numeric==0 and row1.formula_based_criteria==1:
                            data = {"reading_value": row2.get("reading_value")}
                            condition=row1.acceptance_formula 
                            result = frappe.safe_eval(condition, None, data)
                            print(result)
                            if result :
                                pass
                            else:
                                frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")          
                else:
                    pass
        else:
            pass