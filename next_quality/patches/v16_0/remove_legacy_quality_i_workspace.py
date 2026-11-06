"""Remove the legacy "Quality I" workspace.

The module's home workspace is now called "Next Quality" (and is the one the sidebar links to). The
old empty "Quality I" record is not removed by Frappe's own cleanup, so it would linger in the
workspace list. It is only deleted when nothing links to it any more. Idempotent.
"""

import frappe

LEGACY = "Quality I"


def execute():
	if not frappe.db.exists("Workspace", LEGACY):
		return

	if frappe.db.get_value("Workspace", LEGACY, "module") != "Next Quality":
		return

	in_use = frappe.db.exists("Sidebar Item", {"link_type": "Workspace", "link_to": LEGACY}) or frappe.db.exists(
		"Dock Item", {"link_to": LEGACY}
	)
	if in_use:
		return

	frappe.delete_doc("Workspace", LEGACY, force=True, ignore_permissions=True)
