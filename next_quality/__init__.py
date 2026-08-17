# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__version__ = '0.0.1'

try:
    from erpnext.stock import get_item_details
    from erpnext.stock.doctype.quality_inspection.quality_inspection import QualityInspection
    from next_quality.custom_get_item_details import custom_validate_item_details, custom_on_trash

    get_item_details.validate_item_details = custom_validate_item_details
    QualityInspection.on_trash = custom_on_trash
except ImportError:
    pass