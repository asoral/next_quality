frappe.ui.form.on("Batch",{
quality_inspection: function(frm) {
    if (frm.doc.quality_inspection) {
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Quality Inspection",
                name: frm.doc.quality_inspection
            },
            callback: function(r) {
                if (r.message && r.message.readings) {
                    frm.clear_table("test_result");
                    r.message.readings.forEach((d) => {
                        let child = frm.add_child("test_result", d);
                        // Ensure both field mappings for COA Print
                        let coa = d.custom_coa_print_ || d.coa_print || "";
                        child.custom_coa_print_ = coa;
                        child.coa_print = coa;
                    });
                    frm.refresh_field("test_result");
                }
            }
        });
    }
},
refresh:function(frm){
    if(frm.doc.disabled==1){
        frm.add_custom_button(__('Enable Batch'), function() {
                
            let d = new frappe.ui.Dialog({
                fields: [
                    {
                        label: 'Add Comment',
                        fieldname: 'add_comment',
                        fieldtype: 'Small Text',
                        reqd: 1
                    }

                ],
                primary_action_label: 'Submit',
                primary_action(values) {
                    frappe.call({
                        "method": "frappe.desk.form.utils.add_comment",
                        "args": {
                          reference_doctype: frm.doctype,
                          reference_name: frm.docname,
                          content:values.add_comment,
                          comment_email: frappe.session.user,
                          comment_by: frappe.session.user_fullname,
                        }
                    });
                    d.hide();
                    frm.set_value("disabled", 0);
				    frm.refresh_field("disabled");
                    frm.save();

                } 
        });
        d.show();
    });

    }
    if(frm.doc.disabled==0){
        frm.add_custom_button(__('Disable Batch'), function() {
            let d = new frappe.ui.Dialog({
                fields: [
                    {
                        label: 'Add Comment',
                        fieldname: 'add_comment',
                        fieldtype: 'Small Text',
                        reqd: 1
                    }

                ],
                primary_action_label: 'Submit',
                primary_action(values) {
                    frappe.call({
                        "method": "frappe.desk.form.utils.add_comment",
                        "args": {
                          reference_doctype: frm.doctype,
                          reference_name: frm.docname,
                          content:values.add_comment,
                          comment_email: frappe.session.user,
                          comment_by: frappe.session.user_fullname,
                        }
                    });
                    d.hide();
                    frm.set_value("disabled", 1);
				    frm.refresh_field("disabled");
                    frm.save();
                } 
        });
        d.show();
    });
    }
}
});