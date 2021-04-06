frappe.ui.form.on("Work Order", {

    refresh:function(frm){
        if(frm.doc.docstatus == 1 || frm.doc.docstatus == 4){
            var count = 0;
            var temp = ""

            $.each(frm.doc["quality_inspection_parameter"],function(i, quality_inspection_parameter)
            {
                 if(quality_inspection_parameter.inspection_type == "Manual"){
                    if(count == 0){
                        temp = quality_inspection_parameter.inprocess_quality_inspection_template
                    }
                    else{
                        temp += ","+quality_inspection_parameter.inprocess_quality_inspection_template
                    }
                    count += 1;
                 }

            });
            if(count > 0){
            frm.add_custom_button(__('Create Quality Inspection'), function() {
            console.log(count)

            frm.call({
				method: "next_quality.next_quality.custom_work_order.create_inps_qlt_ins",
				args: {
				    doctype: frm.doc.doctype,
				    name: frm.doc.name,
				    production_item: frm.doc.production_item,
				    template: temp
				},
				callback: function(r) {
					if (r.message) {
					    frappe.msgprint(__("Quality Inspection Created"));
					}
				}
                });
				}, __("Create"));  }
        }

    },


    before_save:function(frm){
        frm.clear_table("quality_inspection_parameter");
        frm.call({
				method: "next_quality.next_quality.custom_work_order.get_inprocess_qit",
				args: {
				    bom:frm.doc.bom_no
				},
				callback: function(r) {
				    console.log(r.message)
					if (r.message) {
					    var arr = r.message;
					    for( var i in arr){
                            var childTable = frm.add_child("quality_inspection_parameter");
                            childTable.inprocess_quality_inspection_template = arr[i]['name']
                            childTable.inspection_name=arr[i]['quality_inspection_template_name']
                            childTable.inspection_type = arr[i]['inspection_type']
                            childTable.inspection_applicable_on = arr[i]['inspection_applicable_on']
                            childTable.periodicity = arr[i]['periodicity']

					    }

					}
				}
			});
    },
    before_submit:function(frm){
        frm.call({
            method: "next_quality.next_quality.custom_work_order.set_inq",
				args: {
				   name:frm.doc.name
				},
				callback: function(r) {
				    console.log(r.message)
					if (r.message) {
					    var arr = r.message;
                        for( var i in arr){
                            var childTable = frm.add_child("quality_inspection_parameter");
                            childTable.inprocess_quality_inspection = arr[i]
                            
					    }

					    
					    }

					}
				});
       
    }



});
