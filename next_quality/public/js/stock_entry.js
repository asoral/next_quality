frappe.ui.form.on("Stock Entry", {
    refresh: function(frm){
        if(frm.doc.docstatus == 0 && frm.doc.inspection_required)
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