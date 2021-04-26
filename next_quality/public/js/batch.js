frappe.ui.form.on("Batch",{
refresh:function(frm){
    if(frm.doc.disabled==1){
        frm.add_custom_button(__('Enable Batch'), function() {
                
                
                
        });

    }
}
});