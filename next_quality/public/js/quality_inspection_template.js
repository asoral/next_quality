frappe.ui.form.on("Quality Inspection Template", {

    onload: function(frm) {
		frm.set_query("bom", function() {
			return {
				filters: [
					["is_active","like",1]
				]
			}
		});
	}

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