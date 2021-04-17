frappe.ui.form.on("Material Produce",{
    refresh:function(frm){
        console.log("*******************")
        frm.add_custom_button(__('Quality Inspection'), function() {
            frm.call({
				method:"next_quality.next_quality.custom_material_produce.create_inps",
				args: {
				    work_order:frm.doc.work_order,
				},
				callback: function(r) {
					if (r.message) {
					    frappe.msgprint(__("Quality Inspection Created"));
					}
				}
            });
			frm.set_value("quality_inspection_created", 1);
			frm.refresh_field("quality_inspection_created");
		}, __("Create"));  }   

});
