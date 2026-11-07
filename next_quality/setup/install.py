from next_quality.constants.custom_fields import CUSTOM_FIELDS, PROPERTY_SETTERS
from next_quality.setup.custom_fields import create_property_setters, get_custom_fields_creator

_create_custom_fields = get_custom_fields_creator("Next Quality")


def after_install():
    create_custom_fields()


def after_migrate():
    # keeps the fields in sync with constants/custom_fields.py
    create_custom_fields()


def create_custom_fields():
    # Validation is skipped for faster creation. Fields that already exist are updated.
    _create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)
    create_property_setters(PROPERTY_SETTERS)
