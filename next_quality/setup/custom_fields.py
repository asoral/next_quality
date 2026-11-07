"""Helpers to create, update and remove the custom fields and property setters of this app.

Same approach as India Compliance (`india_compliance/utils/custom_fields.py`): the fields are
defined in Python (`constants/custom_fields.py`), created on install and on every migrate, and
removed again when the app is uninstalled.

Removing a Custom Field deletes its definition only. The database column and its data stay in the
table, so uninstalling and reinstalling an app never loses data.
"""

import functools

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def make_custom_fields(custom_fields, module_name, *args, **kwargs):
    """Create / update custom fields and tag them with the module of the app."""
    for _doctypes, fields in custom_fields.items():
        if isinstance(fields, dict):
            fields = (fields,)

        for field in fields:
            field["module"] = module_name

    return create_custom_fields(custom_fields, *args, **kwargs)


def get_custom_fields_creator(module_name):
    return functools.partial(make_custom_fields, module_name=module_name)


def delete_custom_fields(custom_fields):
    """
    :param custom_fields: a dict like `{'Sales Invoice': [{fieldname: 'test', ...}]}`
    """

    for doctypes, fields in custom_fields.items():
        if isinstance(fields, dict):
            # only one field
            fields = [fields]

        if isinstance(doctypes, str):
            # only one doctype
            doctypes = (doctypes,)

        for doctype in doctypes:
            frappe.db.delete(
                "Custom Field",
                {
                    "fieldname": ("in", [field["fieldname"] for field in fields]),
                    "dt": doctype,
                },
            )

            frappe.clear_cache(doctype=doctype)


def toggle_custom_fields(custom_fields, show):
    """
    Show / hide custom fields

    :param custom_fields: a dict like `{'Sales Invoice': [{fieldname: 'test', ...}]}`
    :param show: True to show fields, False to hide
    """

    for doctypes, fields in custom_fields.items():
        if isinstance(fields, dict):
            fields = [fields]

        if isinstance(doctypes, str):
            doctypes = (doctypes,)

        for doctype in doctypes:
            frappe.db.set_value(
                "Custom Field",
                {
                    "dt": doctype,
                    "fieldname": ["in", [field["fieldname"] for field in fields]],
                },
                "hidden",
                int(not show),
            )

            frappe.clear_cache(doctype=doctype)


def create_property_setters(property_setters):
    """
    :param property_setters: a list of (doctype, fieldname, property, value, property_type, for_doctype)
        tuples, as defined in the PROPERTY_SETTERS constant. `fieldname` is None for DocType level
        properties (`for_doctype=True`).
    """
    from frappe.custom.doctype.property_setter.property_setter import make_property_setter

    changed = set()
    for doctype, fieldname, property, value, property_type, for_doctype in property_setters:
        existing = frappe.db.get_value(
            "Property Setter",
            get_property_setter_name(doctype, fieldname, property),
            ["value", "property_type"],
            as_dict=True,
        )
        if existing and (existing.value or "") == (value or "") and existing.property_type == property_type:
            continue

        make_property_setter(
            doctype,
            fieldname,
            property,
            value,
            property_type,
            for_doctype=for_doctype,
            validate_fields_for_doctype=False,
        )
        changed.add(doctype)

    for doctype in changed:
        frappe.clear_cache(doctype=doctype)


def delete_property_setters(property_setters):
    """Remove exactly the property setters listed in PROPERTY_SETTERS (same tuple format)."""
    for doctype, fieldname, property, *_ in property_setters:
        frappe.db.delete(
            "Property Setter", {"name": get_property_setter_name(doctype, fieldname, property)}
        )
        frappe.clear_cache(doctype=doctype)


def get_property_setter_name(doctype, fieldname, property):
    # same naming as Property Setter.autoname
    return f"{doctype}-{fieldname or 'main'}-{property}"
