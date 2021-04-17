// Copyright (c) 2016, Dexciss Technology and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pending Incoming Quality Inspections"] = {
	"filters": [
        {
			fieldname: "tree_type",
			label: __("Tree Type"),
			fieldtype: "Select",
			options: ["Purchase Reciept"],
			default: "",
			reqd: 1
		},
		{
			fieldname: "item_code",
			label: __("Item Code"),
			fieldtype: "Link",
			options:"Item",
			default: "",
			reqd: 0
		},
		{
			fieldname: "batch_no",
			label: __("Batch Number"),
			fieldtype: "Data",
			default: "",
			reqd: 0
		},
		{
			fieldname: "purchase_receipt",
			label: __("Purchase Receipt"),
			fieldtype: "Link",
			options:"Purchase Receipt",
			default: "",
			reqd: 0
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.defaults.get_global_default("year_start_date"),
			reqd: 0
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.defaults.get_global_default("year_end_date"),
			reqd: 0
        }

	]
};
