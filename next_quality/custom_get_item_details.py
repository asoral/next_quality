import frappe
from frappe import _, throw
from frappe.utils import add_days, add_months, cint, cstr, flt, getdate, parse_json

def custom_validate_item_details(args, item):
	if not args.company:
		throw(_("Please specify Company"))

	from erpnext.stock.doctype.item.item import validate_end_of_life

	validate_end_of_life(item.name, item.end_of_life, item.disabled)

	if cint(item.has_variants):
		msg = f"Item {item.name} is a template, please select one of its variants"

		throw(_(msg), title=_("Template Item Selected"))

	elif args.transaction_type == "buying" and args.doctype != "Material Request":
		if args.get("is_subcontracted")==1:
			if args.get("is_old_subcontracting_flow"):
				if item.is_sub_contracted_item != 1:
					throw(_("Item {0} must be a Sub-contracted Item").format(item.name))
			else:
				if item.is_stock_item:
					throw(_("Item {0} must be a Non-Stock Item").format(item.name))