frappe.ui.form.on("Pick List", {
    setup: function(frm){
        frm.set_query('batch_no', 'locations', (frm, cdt, cdn) => {
			const row = locals[cdt][cdn];
			return {
				query: 'next_quality.custom_methods.get_batch_nos',
				filters: {
					item_code: row.item_code,
					warehouse: row.warehouse,
					sales_order_item:row.sales_order_item
				},
			};
		});
    }
});