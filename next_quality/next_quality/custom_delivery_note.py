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
                                    if float(row2.reading_1) < row1.min_value or float(row2.reading_1) > row1.max_value:
                                        print("********************",row1.specification)
                                        frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")
                                if row1.specification == row2.specification:
                                    if not row2.reading_value and row1.numeric==0 and row1.formula_based_criteria==0 and row1.selection==0:
                                        frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement$")
                                    elif row2.reading_value and row1.value!=row2.reading_value:
                                        if row1.numeric==row2.numeric and row1.formula_based_criteria==row2.formula_based_criteria and row1.selection==row2.selection:
                                            frappe.throw("Please Select another Batch No quality inspection didn't match As per customer requirement")
                                    else:
                                        pass
                                
                                if row1.specification == row2.specification :
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
                                if row1.specification == row2.specification :
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
                                if row1.specification == row2.specification:
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
                            pass
                else:
                    pass
    
# @frappe.whitelist()
# @frappe.validate_and_sanitize_search_inputs
# def get_batch_no(doctype, txt, searchfield, start, page_len, filters):
# 	cond = ""
# 	if filters.get("posting_date"):
# 		cond = "and (batch.expiry_date is null or batch.expiry_date >= %(posting_date)s)"

# 	batch_nos = None
# 	args = {
# 		"item_code": filters.get("item_code"),
# 		"warehouse": filters.get("warehouse"),
# 		"posting_date": filters.get("posting_date"),
# 		"txt": "%{0}%".format(txt),
# 		"start": start,
# 		"page_len": page_len,
# 	}

# 	having_clause = "having sum(sle.actual_qty) > 0"
# 	if filters.get("is_return"):
# 		having_clause = ""

# 	meta = frappe.get_meta("Batch", cached=True)
# 	searchfields = meta.get_search_fields()

# 	search_columns = ""
# 	search_cond = ""

# 	if searchfields:
# 		search_columns = ", " + ", ".join(searchfields)
# 		search_cond = " or " + " or ".join([field + " like %(txt)s" for field in searchfields])

# 	if args.get("warehouse"):
# 		searchfields = ["batch." + field for field in searchfields]
# 		if searchfields:
# 			search_columns = ", " + ", ".join(searchfields)
# 			search_cond = " or " + " or ".join([field + " like %(txt)s" for field in searchfields])

# 		batch_nos = frappe.db.sql(
# 			"""select sle.batch_no, round(sum(sle.actual_qty),2), sle.stock_uom,
# 				concat('MFG-',batch.manufacturing_date), concat('EXP-',batch.expiry_date)
# 				{search_columns}
# 			from `tabStock Ledger Entry` sle
# 				INNER JOIN `tabBatch` batch on sle.batch_no = batch.name
# 			where
# 				batch.disabled = 0
# 				and sle.is_cancelled = 0
# 				and sle.item_code = %(item_code)s
# 				and sle.warehouse = %(warehouse)s
# 				and (sle.batch_no like %(txt)s
# 				or batch.expiry_date like %(txt)s
# 				or batch.manufacturing_date like %(txt)s
# 				{search_cond})
# 				and batch.docstatus < 2
# 				{cond}
# 				{match_conditions}
# 			group by batch_no {having_clause}
# 			order by batch.expiry_date, sle.batch_no desc
# 			limit %(start)s, %(page_len)s""".format(
# 				search_columns=search_columns,
# 				cond=cond,
# 				match_conditions=get_match_cond(doctype),
# 				having_clause=having_clause,
# 				search_cond=search_cond,
# 			),
# 			args,
# 		)

# 	else:
# 		batch_nos= frappe.db.sql(
# 			"""select name, concat('MFG-', manufacturing_date), concat('EXP-',expiry_date)
# 			{search_columns}
# 			from `tabBatch` batch
# 			where batch.disabled = 0
# 			and item = %(item_code)s
# 			and (name like %(txt)s
# 			or expiry_date like %(txt)s
# 			or manufacturing_date like %(txt)s
# 			{search_cond})
# 			and docstatus < 2
# 			{0}
# 			{match_conditions}

# 			order by expiry_date, name desc
# 			limit %(start)s, %(page_len)s""".format(
# 				cond,
# 				search_columns=search_columns,
# 				search_cond=search_cond,
# 				match_conditions=get_match_cond(doctype),
# 			),
# 			args,
# 		)
    
    


    
    
  
    