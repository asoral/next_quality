// Copyright (c) 2021, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Inspection Criteria', {
	quality_inspection_template: function(frm){
        frappe.call({
			method: "get_template_line",
			doc: frm.doc,
			callback: function(r){
			    if(r.message){
			        frm.clear_table("item_quality_inspection_parameter");
                    for (const data of r.message){
                        var row = frm.add_child('item_quality_inspection_parameter');
                        row.specification = data.specification;
                        row.parameter_specification = data.parameter_specification;
                        row.value = data.value;
                        row.number_of_readings = data.number_of_readings;
                        row.numeric = data.numeric;
                        // row.alphanumeric=data.alphanumeric;
                        row.selection=data.selection;
                        row.values = data.values;
                        row.min_value = data.min_value;
                        row.max_value = data.max_value;
                        row.formula_based_criteria = data.formula_based_criteria;
                        row.acceptance_formula = data.acceptance_formula;
                        row.descriptions=data.descriptions;
                        // row.lower_limit = data.lower_limit;
                        // row.upper_limit = data.upper_limit;
                        // row.target_value = data.target_value;
                        // row.uom = data.uom;
                        // row.target_alpha_value = data.target_alpha_value;
                        // row.testing_instructions = data.testing_instructions;
                    }
                    frm.refresh_field('item_quality_inspection_parameter');
			    }
			}
		});
	}
});