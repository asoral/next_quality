
from __future__ import unicode_literals
import frappe
# from erpnext.controllers.queries import get_match_cond
from datetime import datetime

# @frappe.whitelist()
# @frappe.validate_and_sanitize_search_inputs
# def get_batch_nos(doctype, txt, searchfield, start, page_len, filters):
# 	cond = ""
# 	if filters.get("posting_date"):
# 		cond = "and (batch.expiry_date is null or batch.expiry_date >= %(posting_date)s)"

# 	batch_nos_list = []
# 	args = {
# 		'item_code': filters.get("item_code"),
# 		'warehouse': filters.get("warehouse"),
# 		'posting_date': filters.get('posting_date'),
# 		'txt': "%{0}%".format(txt),
# 		"start": start,
# 		"page_len": page_len
# 	}

# 	having_clause = "having sum(sle.actual_qty) > 0"
# 	if filters.get("is_return"):
# 		having_clause = ""

# 	meta = frappe.get_meta("Batch", cached=True)
# 	searchfields = meta.get_search_fields()

# 	search_columns = ''
# 	search_cond = ''

# 	if searchfields:
# 		search_columns = ", " + ", ".join(searchfields)
# 		search_cond = " or " + " or ".join([field + " like %(txt)s" for field in searchfields])

# 	if args.get('warehouse'):
# 		searchfields = ['batch.' + field for field in searchfields]
# 		if searchfields:
# 			search_columns = ", " + ", ".join(searchfields)
# 			search_cond = " or " + " or ".join([field + " like %(txt)s" for field in searchfields])

# 		batch_nos = frappe.db.sql("""select sle.batch_no
# 				from `tabStock Ledger Entry` sle
# 					INNER JOIN `tabBatch` batch on sle.batch_no = batch.name
# 				where
# 					batch.disabled = 0
# 					and sle.item_code = %(item_code)s
# 					and sle.warehouse = %(warehouse)s
# 					and (sle.batch_no like %(txt)s
# 					or batch.expiry_date like %(txt)s
# 					or batch.manufacturing_date like %(txt)s
# 					{search_cond})
# 					and batch.docstatus < 2
# 					{cond}
# 					{match_conditions}
# 				group by batch_no {having_clause}
# 				order by batch.expiry_date, sle.batch_no desc
# 				limit %(start)s, %(page_len)s""".format(
# 			search_columns=search_columns,
# 			cond=cond,
# 			match_conditions=get_match_cond(doctype),
# 			having_clause=having_clause,
# 			search_cond=search_cond
# 		), args)
# 		for res in batch_nos:
# 			if res:
# 				batch_nos_list.append(res)
# 	else:
# 		batch_nos = frappe.db.sql("""select name
# 				from `tabBatch` batch
# 				where batch.disabled = 0
# 				and item = %(item_code)s
# 				and (name like %(txt)s
# 				or expiry_date like %(txt)s
# 				or manufacturing_date like %(txt)s
# 				{search_cond})
# 				and docstatus < 2
# 				{0}
# 				{match_conditions}

# 				order by expiry_date, name desc
# 				limit %(start)s, %(page_len)s""".format(cond, search_columns=search_columns,
# 														search_cond=search_cond,
# 														match_conditions=get_match_cond(doctype)), args)
# 		for res in batch_nos:
# 			if res:
# 				batch_nos_list.append(res)
# 	if filters.get("sales_order_item"):
# 		result = frappe.db.sql("""select tcqi.name  
# 							from `tabSales Order Item` as tsoi
# 							inner join `tabCustomer Quality Inspection` as tcqi on tsoi.name = tcqi.sales_order_line
# 							where tsoi.name = %s and tcqi.docstatus = 1 limit 1""", (filters.get("sales_order_item")))
# 		if result:
# 			lst = []
# 			result1 = frappe.db.sql("""select
# 											tcqi.sales_order_line,tcqi.item
# 											,tqip.specification  
# 											from`tabCustomer Quality Inspection` as tcqi
# 											inner join `tabItem Quality Inspection Parameter` as tqip on tqip.parent = tcqi.name
# 											where tcqi.name = %s """, (result[0][0]), as_dict=True)
# 			for s in result1:
# 				lst.append(s.specification)
# 			if lst:
# 				batch_final_lst = []
# 				for batch in batch_nos_list:
# 					if batch:
# 						batch_insp_ln = frappe.get_all("Quality Inspection Reading", filters={"parent":["=", batch[0]], "specification":["in", lst]}, fields=['name'])
# 						if batch_insp_ln:
# 							batch_i_ln = frappe.get_all("Quality Inspection Reading", filters={"parent": ["=", batch[0]],
# 														"specification": ["in", lst], "status":"Rejected"}, fields=['name'])
# 							if not batch_i_ln:
# 								batch_final_lst.append(batch)
# 				return tuple(batch_final_lst)
# 			else:
# 				return tuple(batch_nos_list)
# 		else:
# 			return tuple(batch_nos_list)
# 	else:
# 		return tuple(batch_nos_list)


def make_customer_quality_insp_submit_time(sl, method):
	if sl:
		for line in sl.items:
				cic = frappe.db.sql("""select name from `tabCustomer Inspection Criteria` 
						where customer = %s and item = %s and docstatus = 1 
					    order by creation desc limit 1""",(sl.customer,line.item_code))
				if cic:
					cic_doc = frappe.get_doc("Customer Inspection Criteria",cic[0][0])
					cqc = frappe.new_doc("Customer Quality Inspection")
					cqc.date = datetime.now().date()
					cqc.sales_order = sl.name
					cqc.sales_order_line = line.name
					cqc.item = cic_doc.item
					cqc.item_name = cic_doc.item_name
					cqc.customer = cic_doc.customer
					cqc.customer_name = cic_doc.customer_name
					cqc.quality_inspection_template = cic_doc.quality_inspection_template
					cqc.item_quality_inspection_parameter = cic_doc.item_quality_inspection_parameter
					cqc.insert(ignore_permissions=True)
					cqc.flags.ignore_validate_update_after_submit = True
					cqc.submit()