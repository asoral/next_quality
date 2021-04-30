frappe.query_reports['Production-Consumption'] = {
    filters: [

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
            fieldname: 't_warehouse',
            label: __('Target Warehouse'),
            fieldtype: 'Link',
            options: 'Warehouse',
        },
        {
            fieldname: 's_warehouse',
            label: __('Source Warehouse'),
            fieldtype: 'Link',
            options: 'Warehouse'
        },
//        {
//            fieldname: 'stock_entry_type',
//            label: __('Stock Entry'),
//            fieldtype: 'Data',
//            "default": "Manufacture"
//        },
        {
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 0,
			"default": frappe.defaults.get_user_default("Company")
		},
//		{
//			"fieldname":"period",
//			"label": __("Period"),
//			"fieldtype": "Select",
//			"options": [
//				{ "value": "Monthly", "label": __("Monthly") },
//				{ "value": "Quarterly", "label": __("Quarterly") },
//				{ "value": "Half-Yearly", "label": __("Half-Yearly") },
//				{ "value": "Yearly", "label": __("Yearly") }
//			],
//			"default": "Monthly"
//		},
        {
			"fieldname":"fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options":'Fiscal Year',
			"reqd": 0,
			"default": frappe.sys_defaults.fiscal_year
		},
//		{
//			"fieldname":"based_on",
//			"label": __("Based On"),
//			"fieldtype": "Data",
//			"options": [
//				{ "value": "dcs", "label": __("DCS") },
//				{ "value": "milk_type", "label": __("Milk Type") }
//			],
//			"default": "dcs"
//		},
        {
			"fieldname":"group_by",
			"label": __("Group By"),
			"fieldtype": "Select",
			"options": [
			{ "value": "all", "label": __("None") },
				{ "value": "manufacture", "label": __("Work Order") },
                { "value": "trxtype", "label": __("Prod. Item") },
			],
			"default": "None"
		},
    ]
}