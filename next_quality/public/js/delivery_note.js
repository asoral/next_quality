frappe.ui.form.on("Delivery Note", {
    refresh: function(frm){
        set_batch_filter(frm)
        if(frm.doc.docstatus == 0)
        {
            frm.add_custom_button(__("Make Quality Inspection"), function() {
                frappe.call({
                    method: 'next_quality.next_quality.custom_quality_inspection.make_stock_quality_inspec',
                    args: {
                        "doc_name" : frm.doc.name,
                        "doctype" : frm.doctype
                    },
                    callback: function(r) {
                        if (r.message)
                        {
                            frappe.set_route('List',"Quality Inspection",{'reference_name': frm.doc.name});
                        }
                    }
                });
            },'Create');
        }
    }
});
// frappe.ui.form.on("Delivery Note Item", {
//     batch_no: function(frm){
//         set_batch_filter(frm)
//     }
// });

// function set_batch_filter(frm){
//     frm.set_query('batch_no', 'items', (frm, cdt, cdn) => {
//         const row = locals[cdt][cdn];
//         return {
//             query: 'next_quality.custom_methods.get_batch_nos',
//             filters: {
//                 item_code: row.item_code,
//                 warehouse: row.warehouse,
//                 posting_date:row.posting_date,
//                 sales_order_item:row.so_detail
//             },
//         };
//     });

// }