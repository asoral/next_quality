frappe.ui.form.on("Item", {
    onload:function(frm){
        frm.call({
				method: "next_quality.next_quality.custom_item.show_inprocess_template",
				callback: function(r) {
				    console.log(r.message)
					if (r.message) {
					    frm.set_query("quality_inspection_template", function() {
			                return {
				                filters: [
					                ["name", "in", r.message]
				                ]
			                }
		                });
	                }
				}

		});
    }

});