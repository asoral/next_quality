frappe.ui.form.on("Purchase Receipt",{
	refresh:function(frm,cdt,cdn){
		
		frappe.model.with_doc('Purchase Receipt Item',{"parent":frm.doc.name},function () {
            let d = frappe.model.get_doc('Purchase Receipt Item', {"parent":frm.doc.name});
			if(frm.doc.docstatus == 0){
				frm.add_custom_button(__("Quality Inspection"), function() {
					if(d.quality_inspection_created==0){
						frappe.call({
							method: 'next_quality.next_quality.custom_purchase_receipt.create_quality_inspection',
							args: {
								"doc_name" : frm.doc.name
							},
							callback: function(r) {
								if (r.message) {
									frappe.msgprint(__("Quality Inspection Created"));
								}
							}
						});
					}
					else{
						frappe.confirm('Are you want to Create Duplicate Quality Inspection?',
						() => {
							frappe.call({
								method: 'next_quality.next_quality.custom_purchase_receipt.create_quality_inspection',
								args: {
									"doc_name" : frm.doc.name
								},
								callback: function(r) {
									if (r.message) {
										frappe.msgprint(__("Quality Inspection Created"));
									}
								}
							});
						}, () => {
							frm.save();
						})
					}
				}, 'Create');
			}
		});
	}
});

