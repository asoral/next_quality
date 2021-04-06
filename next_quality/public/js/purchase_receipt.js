frappe.ui.form.on("Purchase Receipt",{
    refresh:function(frm){
            frm.add_custom_button(__('Quality Inspection'), function() {
            frm.call({
				method: "next_quality.next_quality.custom_purchase_receipt.create_quality_inspection",
//				freeze: true,
//				freeze_message: __("Creating quality_inspection"),
				args: {
				    doc_name: frm.doc.name
				},
				callback: function(r) {
					if (r.message) {
					    frappe.msgprint(__("Quality Inspection Created"));
					}
				}
                });
				}, __("Create"));  }

});