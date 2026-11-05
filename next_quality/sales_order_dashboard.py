from frappe import _


def get_data(data):
	"""Extend the standard Sales Order dashboard with Customer Quality Inspection."""
	if not any(group.get("label") == _("Customer Quality Inspection") for group in data.get("transactions", [])):
		data.setdefault("transactions", []).append(
			{"label": _("Customer Quality Inspection"), "items": ["Customer Quality Inspection"]}
		)
	return data
