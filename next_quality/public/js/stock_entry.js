frappe.ui.form.on("Stock Entry", {
    refresh: function(frm){
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
                            frm.reload()
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
    }
});

