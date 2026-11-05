from frappe import _


def get_data(data):
	"""Extend the standard Customer dashboard with Customer Inspection Criteria."""
	if not any(group.get("label") == _("Customer Inspection Criteria") for group in data.get("transactions", [])):
		data.setdefault("transactions", []).append(
			{"label": _("Customer Inspection Criteria"), "items": ["Customer Inspection Criteria"]}
		)
	return data
