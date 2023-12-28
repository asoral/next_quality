frappe.ui.form.on("Sales Order", {
    refresh: function(frm){
        if(frm.doc.docstatus == 1){
            frm.add_custom_button(__("Customer Quality Inspection"), function() {
                frappe.call({
                method: 'next_quality.next_quality.custom_quality_inspection.make_quality_inspection',
                args: {
                    "doc_name" : frm.doc.name
                },
                callback: function(r) {
                    if (r.message) {
                        var doclist = frappe.model.sync(r.message);
                        frappe.set_route('Form',doclist[0].doctype, doclist[0].name);
                    }
                }
            });
			}, 'Create');
        }
    }
});