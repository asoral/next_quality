// Copyright (c) 2020, Dexciss Technology Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Quality Inspection Creation Tool',{
	refresh: function(frm){
		frm.disable_save();
		//frm.remove_custom_button("Get Item From Purchase Receipt");
		$(".menu-btn-group").hide()
		frm.page.set_primary_action(__('Make Quality Inspection'), () => {
			let btn_primary = frm.page.btn_primary.get(0);
			return frm.call({
				doc: frm.doc,
				btn: $(btn_primary),
				method: "make_quality_inspection",
				// freeze_message: __("Creating {0} quality_inspection", [frm.doc.invoice_type])
				callback: function (r) {	
					if(r.message){	
						frappe.msgprint({
							title: __('Notification'),
							indicator: 'green',
							message: __('Quality inspection created successfully')
						});
					}	
				},
			});
		});
		cur_frm.cscript.get_item_from_purchase_receipt = function(doc) {
			fetch_data(frm,"Purchase Receipt Item","Purchase Receipt")
		},

		cur_frm.cscript.get_item_from_purchase_invoice = function(doc) {
			fetch_data(frm,"Purchase Invoice Item","Purchase Invoice")
		},

		cur_frm.cscript.get_item_from_delivery_note = function(doc) {
			fetch_data(frm,"Delivery Note Item","Delivery Note")
		},
		
		cur_frm.cscript.get_item_from_sales_invoice = function(doc) {
			fetch_data(frm,"Sales Invoice Item","Sales Invoice")
		},

		cur_frm.cscript.get_item_from_stock_entry = function(doc) {
			fetch_data(frm,"Stock Entry Detail","Stock Entry")
		}

	},
	inspection_type: function(frm) {
	if(frm.doc.inspection_type == "Incomming")
  	{	
    	set_field_options("reference_type", ["Purchase Receipt", "Purchase Invoice"])
  	}
  	else if(frm.doc.inspection_type == "Outgoing")
  	{
    	set_field_options("reference_type", ["Delivery Note","Sales Invoice"])
  	}
  	else if(frm.doc.inspection_type == "In Process")
  	{
    	set_field_options("reference_type", ["Stock Entry"])
	  }
	else if(frm.doc.inspection_type == "")
  	{
    	set_field_options("reference_type", ["Purchase Receipt", "Purchase Invoice","Delivery Note","Sales Invoice","Stock Entry"])
  	}
	},
});

function fetch_data(frm, args_doc,reference_doc){
	frappe.call({
		doc: frm.doc,
		method: "get_item_from_doc",
		args: {
			doc: args_doc
		},
		callback: function (r) {
		    frm.clear_table("inspections_to_be_created");
			r.message.map(item => {
				frm.add_child('inspections_to_be_created', {
					reference_doc: reference_doc,
					item:item.item_code,
					description:item.description,
					serial_no:item.serial_no,
					batch_no: item.batch_no,
					quality_inspection_template: item.template,
					sample_size:1,
					reference_name: item.parent,
					supplier_name: item.supplier,
					destination_warehouse: item.destination_warehouse,
					source_warehouse : item.source_warehouse,
					customer_name : item.customer,
					quality_inspection_template: item.template,
					qty: item.qty
				});
			})
			frm.refresh_field('inspections_to_be_created');	
		},
	})
}
	