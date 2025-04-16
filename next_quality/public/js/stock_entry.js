frappe.ui.form.on("Stock Entry", {
    refresh: function(frm){
        frm.set_df_property("inspection_required", "hidden", 1);
        frappe.call({
			method: "next_quality.next_quality.custom_stock_entry.get_list",
			args: {
				company: frm.doc.company,
			},
			callback: function (r) {
				console.log(r.message)
				if (r.message) {
					frm.set_query("reference_challan", function () {
						return {
							filters: [
								["name", "in", r.message]
							]
						}
					});
				}
			}

		});
        

        if(frm.doc.docstatus == 0 && frm.doc.inspection_required)
        {
            frm.add_custom_button(__("Make Quality Inspection"), function() {
                frappe.call({
                    method: 'next_quality.next_quality.custom_quality_inspection.make_stock_quality_inspec',
                    args: {
                        "doc_name" : frm.doc.name,
                        "doctype" : frm.doctype
                    },
                    callback: function(r) {
                        if (r.message)
                        {
                            frappe.msgprint(__("Quality Inspection Created"));
                        }
                    }
                });
            
  
            },'Create');
        }
        
        if (frm.doc.stock_entry_type === "Manufacture"){
           
            frm.add_custom_button(__('On Finish Create Quality Inspection'), function() {
                if(frm.doc.custom_quality_inspection_created==1)
                    {	
                        frappe.msgprint(__("Quality Inspection already Created"));
                    }
                else{
                frm.call({
                    method: "next_quality.next_quality.custom_stock_entry.create_quality_inspection",
                    args: {
                        doctype: frm.doc.doctype,
                        name: frm.doc.name,
                        work_order:frm.doc.work_order
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(__("Quality Inspection Created"));
                            frm.reload_doc();
                        }
                    }
                    });
         }
        
				}); 
        frm.set_df_property("custom_on_finish_inspection_required", "hidden", 0);
        frm.refresh_fied("custom_on_finish_inspection_required")
        }
        else{
            frm.set_df_property("custom_on_finish_inspection_required", "hidden", 1);
        }
    },
    get_items: function () {
		var me = this;
		if (!this.frm.doc.fg_completed_qty || !this.frm.doc.bom_no)
			frappe.throw(__("BOM and Manufacturing Quantity are required"));

		if (this.frm.doc.work_order || this.frm.doc.bom_no) {
			// if work order / bom is mentioned, get items
			return this.frm.call({
				doc: me.frm.doc,
				freeze: true,
				method: "get_items",
				callback: function (r) {
					if (!r.exc) refresh_field("items");
					if (me.frm.doc.bom_no) attach_bom_items(me.frm.doc.bom_no)
				}
			});
		}
	},
});

function attach_bom_items(bom_no) {
	if (!bom_no) {
		return
	}

	if (check_should_not_attach_bom_items(bom_no)) return
	frappe.db.get_doc("BOM", bom_no).then(bom => {
		const { name, items } = bom
		erpnext.stock.bom = { name, items: {} }
		items.forEach(item => {
			erpnext.stock.bom.items[item.item_code] = item;
		});
	});
}