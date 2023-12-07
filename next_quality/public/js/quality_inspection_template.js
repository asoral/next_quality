frappe.ui.form.on("Quality Inspection Template", {

    onload: function(frm) {
		frm.set_query("bom", function() {
			return {
				filters: [
					["is_active","like",1]
				]
			}
		});
	},
	setup:function(frm){
        frm.call({
			method:"next_quality.next_quality.custom_quality_inspection_template.get_list",
			args:{
					"select_intermediate_bom_to_copy_results_from":frm.doc.select_intermediate_bom_to_copy_results_from
			},
			callback: function(r) {
				if (r.message) {
					frm.set_query("select_intermediate_bom_to_copy_results_from", function() {
						return {
							filters: [
								["name", "in",r.message]
							]
						}
					});
				}
			}
        });

	},   
	

});

frappe.ui.form.on(' Quality Inspection Template', {
	 quality_inspection_template_parameters_add: function(frm,cdt,cdn){
	    var child = locals[cdt][cdn];
	    if(frm.doc.inspection_applicable_on == "Job Card"){
	        frappe.model.set_value(cdt,cdn,"on_job_card",1);
	        frm.refresh_fields();
	    }
	 },

});