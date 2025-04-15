# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__version__ = '0.0.1'
from erpnext.stock import get_item_details
from next_quality.custom_get_item_details import custom_validate_item_details

get_item_details.validate_item_details = custom_validate_item_details