"""Desk navigation helpers (Apps screen visibility)."""

import frappe

# the app is listed on the Apps screen for users who can read at least one of these DocTypes
APP_DOCTYPES = ('Customer Inspection Criteria', 'Customer Quality Inspection')


def check_app_permission():
	"""Show the app on the Apps screen only to users who can open something in it."""
	if frappe.session.user == "Administrator":
		return True

	# Website Users cannot open desk routes, so do not offer them the app
	if frappe.get_cached_value("User", frappe.session.user, "user_type") == "Website User":
		return False

	return any(frappe.has_permission(doctype, "read") for doctype in APP_DOCTYPES)
