frappe.ui.form.on("Job Card", {
    create_quality_inspection:function(frm){
        if(frm.doc.status == "Work In Progress" ){
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
             }
        }
    },

    onload:function(frm){
        frm.clear_table("quality_inspection_parameter");
        frm.call({
				method: "next_quality.next_quality.custom_job_card.get_inprocess_qite",
				args: {
				    bom:frm.doc.bom_no,
				    workstation:frm.doc.workstation
				},
				callback: function(r) {
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
					    frm.refresh_field("quality_inspection_parameter");
					}
				}
			});
    },

    before_submit:function(frm){
        console.log("job card",frm.doc.job_started);
        if(frm.doc.job_started == 1){
            var count = 0;
            var temp = ""

            $.each(frm.doc["quality_inspection_parameter"],function(i, quality_inspection_parameter)
            {
                 if(quality_inspection_parameter.inspection_type == "On Start"){
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
            }
        }
    },
    on_submit:function(frm){
        console.log("job card",frm.doc.job_started);
        if(frm.doc.status=="Completed"){
            var count = 0;
            var temp = ""

            $.each(frm.doc["quality_inspection_parameter"],function(i, quality_inspection_parameter)
            {
                 if(quality_inspection_parameter.inspection_type == "On Finish"){
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
            }
        }
    }



});