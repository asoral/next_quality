frappe.query_reports["Production-Consumption"] = {
	"filters": [

        {
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 0,
			"default": frappe.defaults.get_user_default("Company")
		},
        {
            fieldname: 'item_code',
            label: __('Prod. Item'),
            fieldtype: "Link",
            options: "Item"
        },
        {
            fieldname: 'serial_number',
            label: __('Serial'),
            fieldtype: 'Link',
            options: "Serial No"
        },
         {
            fieldname: 'batch_number',
            label: __('Batch'),
            fieldtype: 'Link',
            options: "Batch"
        },
        {
            fieldname: 'item_group',
            label: __('Item Group'),
            fieldtype: 'Link',
            options: "Item Group"
        },
        {
            fieldname: 'brand',
            label: __('Brand'),
            fieldtype: 'Link',
            options: "Brand"
        },
        {
            fieldname: 'warehouse',
            label: __('Warehouse'),
            fieldtype: 'Link',
            options: 'Warehouse',
        },
        {
            fieldname: 'work_order',
            label: __('Work Order'),
            fieldtype: 'Link',
            options: 'Work Order',
        },
        {
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			reqd: 0
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 0
        },
        // {
		// 	fieldname: "tree_type",
		// 	label: __("Tree Type"),
		// 	fieldtype: "Select",
		// 	options: ["Work Order" , "Prod. Item"],
		// 	default: "Work Order",
		// 	reqd: 1
		// },
        // {
		// 	"fieldname":"group_by",
		// 	"label": __("Group By"),
		// 	"fieldtype": "Select",
		// 	"options": [
		// 	{ "value": "all", "label": __("None") },
		// 	{ "value": "manufacture", "label": __("Work Order") },
        //     { "value": "trxtype", "label": __("Prod. Item") },
		// 	],
		// 	"default": "None"
		// },
        // {
            //            fieldname: 'stock_entry_type',
            //            label: __('Stock Entry'),
            //            fieldtype: 'Data',
            //            "default": "Manufacture"
            //        },
                
        // {
        //     "fieldname":"period",
        //     "label": __("Period"),
        //     "fieldtype": "Select",
        //     "options": [
        //         { "value": "Monthly", "label": __("Monthly") },
        //         { "value": "Quarterly", "label": __("Quarterly") },
        //         { "value": "Half-Yearly", "label": __("Half-Yearly") },
        //         { "value": "Yearly", "label": __("Yearly") }
        //     ],
        //     "default": "Monthly"
        // },
    ]
}