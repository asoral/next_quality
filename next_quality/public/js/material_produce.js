frappe.ui.form.on("Material Produce",{
    refresh:function(frm){
		frappe.model.get_value('Quality Inspection Template', {"bom":frm.doc.bom}, 'copy_quality_inspection',
  		function(d) {
  		if(d.copy_quality_inspection==0){
			if(frm.doc.docstatus==0){
        		frm.add_custom_button(__('Quality Inspection'), function() {
					if(frm.doc.quality_inspection_created==1)
					{	
						frappe.msgprint(__("Quality Inspection already Created"));
					}
					else{
            		frm.call({
					method:"next_quality.next_quality.custom_material_produce.create_inps",
					args: {
				    	work_order:frm.doc.work_order,
						name:frm.doc.name,
					},
					callback: function(r) {
						if (r.message) {
					    	frappe.msgprint(__("Quality Inspection Created"));
							frm.set_value("quality_inspection", r.message)
							frm.save();
						}
					}
            	});
			}
				frm.set_value("quality_inspection_created", 1);
				frm.refresh_field("quality_inspection_created");
				frm.save();

		}, __("Create"));  }
		}
		else if(d.copy_quality_inspection==1){
			if(frm.doc.docstatus==0){
				frm.add_custom_button(__('Copy Quality Inspection'), function() {
					if(frm.doc.quality_inspection_created==1)
					{	
						frappe.msgprint(__("Quality Inspection already Created"));
					}
					else{
					frm.call({
					method:"next_quality.next_quality.custom_material_produce.copy_inps",
					args: {
					work_order:frm.doc.work_order,
					bom:frm.doc.bom,
					item_name:frm.doc.item_name,
					name:frm.doc.name
					},
					callback: function(r) {
						if (r.message) {
							frappe.msgprint(__("Quality Inspection Created"));
							frm.set_value("quality_inspection", r.message)
							frm.save()
						}
					}
				});
				}
				frm.set_value("quality_inspection_created", 1);
				frm.refresh_field("quality_inspection_created");
				frm.save();
	}, __("Create"));  }
	}
	})
	}
	
});
