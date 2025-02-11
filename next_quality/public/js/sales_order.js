frappe.ui.form.on("Sales Order", {
    refresh: function(frm){
        console.log("Trigger Sales Order------");

        if (frm.doc.company) {
            frm.set_query('department', function() {
                return {
                    filters: {
                        company: frm.doc.company
                    }
                };
            });
        }

        if (frm.doc.company === "Subhash Chemical Industries Pvt Ltd") {
            frm.set_query("set_warehouse", function() {
                return {
                    filters: {
                        name: ["in",["FG UNIT 1 - SCIPL", "FG UNIT 2 - SCIPL", "PACKING UNIT 1 - SCIPL", "PACKING UNIT 2 - SCIPL"] ]
                    }
                };
            });
        }

        if (frm.doc.company === "JORINCO SPECIALITIES PVT LTD.") {
            frm.set_query("set_warehouse", function() {
                return {
                    filters: {
                        name: ["in", ["FG - JSPL", "PACKING - JSPL"]]
                    }
                };
            });
        }
        if(frm.doc.docstatus == 1){
            frm.add_custom_button(__("Customer Quality Inspection"), function() {
                frappe.call({
                method: 'next_quality.next_quality.custom_quality_inspection.make_quality_inspection',
                args: {
                    "doc_name" : frm.doc.name
                },
                callback: function(r) {
                    if (r.message) {
                        var doclist = frappe.model.sync(r.message);
                        frappe.set_route('Form',doclist[0].doctype, doclist[0].name);
                    }
                }
            });
			}, 'Create');
        }
    }
});