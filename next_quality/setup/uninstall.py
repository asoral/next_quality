from next_quality.constants.custom_fields import CUSTOM_FIELDS, PROPERTY_SETTERS
from next_quality.setup.custom_fields import delete_custom_fields, delete_property_setters


def before_uninstall():
    delete_custom_fields(CUSTOM_FIELDS)
    delete_property_setters(PROPERTY_SETTERS)
