__version__ = "0.0.1"

from erpnext.stock import get_item_details
from erpnext.stock.doctype.quality_inspection.quality_inspection import QualityInspection

from next_quality.custom_get_item_details import custom_on_trash, custom_validate_item_details

get_item_details.validate_item_details = custom_validate_item_details
QualityInspection.on_trash = custom_on_trash