frappe.ui.form.on("Customer", {
    refresh: function(frm){
        frm.add_custom_button(__("Customer Quality Criteria"), function() {
            frappe.call({
            method: 'next_quality.next_quality.custom_quality_inspection.make_quality_criteria',
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
});