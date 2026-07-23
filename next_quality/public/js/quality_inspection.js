
frappe.ui.form.on("Quality Inspection", {

	refresh:function(frm){
		if(frm.is_new() && frm.doc.quality_inspection_template && 
            (!frm.doc.readings || frm.doc.readings.length === 0 || !frm.doc.readings[0].custom_coa_print_)) {
			frm.trigger("quality_inspection_template");
		}
		$.each(frm.doc["readings"],function(i,row)
            {
				if(frm.doc.accepted_under_deviation==1){
					row.status="Accepted"
					frm.doc.status="Accepted"
					refresh_field("readings");
					refresh_field("status")
				}
			})
			
		setTimeout(() => {
			render_custom_readings_table(frm);
		}, 500);
	},
    
    quality_inspection_template: function(frm) {
		if (frm.doc.quality_inspection_template) {
			frm.call({
				
				method: "next_quality.next_quality.custom_quality_inspection.get_item_specification_details",
				args: {
                    quality_inspection_template: frm.doc.quality_inspection_template,
                    item_code: frm.doc.item_code
                  },
				callback: function(r) {
				    if (r.message && r.message.length > 0) {
                        frm.clear_table('readings');
						r.message.forEach((d) => {
							var child = frm.add_child("readings");
							// Copy specific fields, exclude internal frappe fields like name, parent
							Object.keys(d).forEach(k => {
								if(!["name", "parent", "parentfield", "parenttype", "owner", "idx", "creation", "modified", "modified_by", "doctype", "docstatus"].includes(k)) {
									child[k] = d[k];
								}
							});
							
							// Ensure both field mappings work in JS as well
							if(d.custom_coa_print_) {
								child.custom_coa_print_ = d.custom_coa_print_;
								child.coa_print = d.custom_coa_print_;
							}
							
							if(!child.status) {
								child.status = "Accepted";
							}
						});
						// Do NOT refresh_field() here - it breaks inline editing and causes fields to disappear
						setTimeout(() => {
							render_custom_readings_table(frm);
						}, 500);
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
	// onload:function(frm,cdt,cdn){
	// 		console.log("*******************")
	// 		 frm.call({
	// 			method:"next_quality.next_quality.custom_quality_inspection.get_parameter_values",
	// 			args: {
	// 				"quality_inspection_template_name":frm.doc.quality_inspection_template
	// 			},
	// 			callback: function(r)
	// 			{
	// 				console.log(r.message)
	// 				var child = locals[cdt][cdn].readings;
	// 				if (r.message) {
	// 				//    frappe.utils.filter_dict(frm.fields_dict["readings"].grid.docfields, {"fieldname": "parameter_value"})[0].options = r.message;
	// 				frappe.meta.get_docfield("Quality Inspection Reading","parameter_value").options = r.message
	// 				// frm.set_df_property('parameter_value','options',r.message);


	// 				}
	// 				refresh_field("readings");
	// 			}
	// 		});
	// 	 },
		
		
});

frappe.ui.form.on("Quality Inspection Reading",{

	refresh: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		if (!child) return;
		
		var g = frm.fields_dict.readings && frm.fields_dict.readings.grid;
		if (!g) return;

		// Force reading_value and parameter_value to be visible and editable
		g.update_docfield_property('reading_value', 'hidden', 0);
		g.update_docfield_property('reading_value', 'read_only', 0);
		g.update_docfield_property('reading_value', 'depends_on', '');
		
		g.update_docfield_property('parameter_value', 'hidden', 0);
		g.update_docfield_property('parameter_value', 'read_only', 0);
		
		g.update_docfield_property('acceptance_formula', 'hidden', 0);
		g.update_docfield_property('acceptance_formula', 'read_only', 1);
	},

	form_render: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		if (!child || !child.values) {
			return;
		}

		try {
			var obj = JSON.parse(child.values);
			if (!Array.isArray(obj)) return;
			
			var b = [''];
			for (var i = 0; i < obj.length; i++) {
				if (obj[i] && obj[i].value !== undefined) {
					b.push(obj[i].value);
				}
			}
			frm.fields_dict.readings.grid.update_docfield_property('parameter_value', 'options', b);
		} catch (e) {
			console && console.warn('Quality Inspection Reading: invalid values JSON', e);
		}
	}
});

function render_custom_readings_table(frm) {
    // Hide the original readings grid/table entirely (including the "Add Row" button)
    frm.toggle_display("readings", false);

    let $html_field = frm.get_field("readings_html");
    if (!$html_field) return;

    let $wrapper = $html_field.$wrapper;
    $wrapper.find('.custom-qi-table-wrapper').remove();

    if (!frm.doc.readings || frm.doc.readings.length === 0) {
        return;
    }
    
    let html = `
    <style>
        .custom-qi-table { width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 20px; font-size: 12px; }
        .custom-qi-table th, .custom-qi-table td { border: 1px solid #d1d8dd; padding: 5px; text-align: left; }
        .custom-qi-table th { background-color: #f8f9fa; font-weight: bold; }
        .custom-qi-table input, .custom-qi-table select { width: 100%; padding: 4px; border: 1px solid #d1d8dd; border-radius: 4px; font-size: 12px; border-color: #d1d8dd !important; }
        .custom-qi-table input:focus, .custom-qi-table select:focus { outline: none; border-color: #1f272e !important; }
    </style>
    <div class="custom-qi-table-wrapper" style="overflow-x: auto;">
        <table class="custom-qi-table">
            <thead>
                <tr>
                    <th style="width: 30px;">No.</th>
                    <th style="width: 150px;">Parameter</th>
                    <th style="width: 100px;">Status</th>
                    <th style="width: 150px;">Acceptance Criteria</th>
                    <th style="width: 80px;">Minimum</th>
                    <th style="width: 80px;">Maximum</th>
                    <th style="width: 80px;">COA Print</th>
                    <th style="width: 100px;">Reading</th>
                    <th style="width: 100px;">Reading 1</th>
                    <th style="width: 100px;">Reading 2</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    frm.doc.readings.forEach((row, idx) => {
        let status_opts = ["Accepted", "Rejected"];
        let status_html = `<select data-idx="${idx}" data-field="status" data-cdn="${row.name}">
            ${status_opts.map(opt => `<option value="${opt}" ${row.status===opt ? 'selected' : ''}>${opt}</option>`).join('')}
        </select>`;
        
        let coa_opts = ["Yes", "No"];
        let coa_val = row.custom_coa_print_ || row.coa_print || "";
        let coa_html = `<select data-idx="${idx}" data-field="custom_coa_print_" data-cdn="${row.name}">
            <option value=""></option>
            ${coa_opts.map(opt => `<option value="${opt}" ${coa_val===opt ? 'selected' : ''}>${opt}</option>`).join('')}
        </select>`;

        let reading_val = row.reading_value || row.parameter_value || "";
        let reading_html = `<input type="text" data-idx="${idx}" data-field="reading_value" data-cdn="${row.name}" value="${reading_val}">`;
        
        html += `
                <tr>
                    <td>${idx + 1}</td>
                    <td>${row.specification || ''}</td>
                    <td>${status_html}</td>
                    <td>${row.acceptance_formula || row.acceptance_criteria || row.value || ''}</td>
                    <td>${row.min_value !== undefined && row.min_value !== null ? row.min_value : ''}</td>
                    <td>${row.max_value !== undefined && row.max_value !== null ? row.max_value : ''}</td>
                    <td>${coa_html}</td>
                    <td>${reading_html}</td>
                    <td><input type="text" data-idx="${idx}" data-field="reading_1" data-cdn="${row.name}" value="${row.reading_1 || ''}"></td>
                    <td><input type="text" data-idx="${idx}" data-field="reading_2" data-cdn="${row.name}" value="${row.reading_2 || ''}"></td>
                </tr>
        `;
    });
    
    html += `
            </tbody>
        </table>
    </div>
    `;
    
    $wrapper.append(html);
    
    // Attach events
    $wrapper.find('.custom-qi-table input, .custom-qi-table select').on('change', function() {
        let $el = $(this);
        let field = $el.attr('data-field');
        let cdn = $el.attr('data-cdn');
        let val = $el.val();
        
        frappe.model.set_value("Quality Inspection Reading", cdn, field, val);
        
        if(field === 'reading_value') {
            frappe.model.set_value("Quality Inspection Reading", cdn, "parameter_value", val);
        }
    });
}