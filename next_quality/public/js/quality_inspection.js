let df_status=frappe.meta.get_docfield("Quality Inspection Reading", "status", cur_frm.doc.name)

frappe.ui.form.on("Quality Inspection", {
    
    quality_inspection_template: function(frm) {
		if (frm.doc.quality_inspection_template) {
			frm.call({
				method: "next_quality.next_quality.custom_quality_inspection.get_item_specification_details",
				args: {
                    quality_inspection_template: frm.doc.quality_inspection_template,
                    item_code: frm.doc.item_code
                  },
				callback: function(r) {
				    if (r.message) {
                        frm.clear_table('readings');
						r.message.forEach((d) => {
							frm.add_child("readings", d);
						});
						refresh_field("readings");
					}
				}
			});
		}
	},
	inspection_type: function(frm) {
		if(frm.doc.inspection_type == "Incoming")
		  {
			set_field_options("reference_type", ["Purchase Receipt", "Purchase Invoice"])
		  }
		  else if(frm.doc.inspection_type == "Outgoing")
		  {
			set_field_options("reference_type", ["Delivery Note","Sales Invoice"])
		  }
		  else if(frm.doc.inspection_type == "In Process")
		  {
			set_field_options("reference_type", ["Stock Entry","Work Order","Job Card"])
		  }
		else if(frm.doc.inspection_type == "")
		  {
			set_field_options("reference_type", ["Purchase Receipt", "Purchase Invoice","Delivery Note","Sales Invoice","Stock Entry"])
		  }
		},
	onload:function(frm){
			frm.call({
				method: "next_quality.next_quality.custom_quality_inspection.get_parameter_values",
				args: {
					"quality_inspection_template":quality_inspection_template_name
	
	
				},
				callback: function(r){
					if (r.message) {
						console.log(r.message)
						frappe.utils.filter_dict(frm.fields_dict["readings"].grid.docfields, {"fieldname": "parameter_values"}).options = r.message;
						// frm.set_df_property("parameter_values","options", ["ajay","Ujjwal"]);
						// frm.refresh_field("parameter_values")
						// frappe.meta.get_docfield('Quality Inspection Reading', 'parameter_values',frm.doc.name).options = r.message;
	
						// frappe.meta.get_docfield('Quality Inspection Reading', 'parameter_values').options = r.message;
	
						// set_field_options("readings","parameter_values", r.message)
						frm.refresh_field("parameter_values")
					}
					// frm.refresh_field("readings")
					
					
				}
			})
		}
});

// frappe.ui.form.on("Quality Inspection Reading",{
// 	form_render:function(frm){
//         frm.call({
// 		    method: "next_quality.next_quality.custom_quality_inspection.get_parameter_values",
// 		    args: {
// 				specification:"specification"


// 			},
// 			callback: function(r){
// 				if (r.message) {
// 					console.log(r.message)
// 					frappe.utils.filter_dict(frm.fields_dict["readings"].grid.docfields, {"fieldname": "parameter_values"}).options = r.message;
// 					// frm.set_df_property("parameter_values","options", ["ajay","Ujjwal"]);
// 					// frm.refresh_field("parameter_values")
// 					// frappe.meta.get_docfield('Quality Inspection Reading', 'parameter_values',frm.doc.name).options = r.message;

// 					// frappe.meta.get_docfield('Quality Inspection Reading', 'parameter_values').options = r.message;

// 					// set_field_options("readings","parameter_values", r.message)
// 					frm.refresh_field("parameter_values")
// 				}
// 				// frm.refresh_field("readings")
				
				
// 			}
//         })
		
//     },
	
// });