from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import today
from erpnext.stock.doctype.pick_list.pick_list import PickList, get_available_item_locations_for_serial_and_batched_item, get_items_with_location_and_quantity, get_available_item_locations_for_serialized_item, get_available_item_locations_for_other_item

class CustomPickList(PickList):
    pass
#     def set_item_locations(self, save=False):
#         items = self.aggregate_item_qty()
#         self.item_location_map = frappe._dict()

#         from_warehouses = None
#         if self.parent_warehouse:
#             from_warehouses = frappe.db.get_descendants('Warehouse', self.parent_warehouse)

#         # Create replica before resetting, to handle empty table on update after submit.
#         locations_replica = self.get('locations')

#         # reset
#         self.delete_key('locations')
#         for item_doc in items:
#             item_code = item_doc.item_code

#             self.item_location_map.setdefault(item_code,
#                     get_available_item_locations(item_code, from_warehouses, self.item_count_map.get(item_code), self.company,False,item_doc))

#             locations = get_items_with_location_and_quantity(item_doc, self.item_location_map, self.docstatus)

#             item_doc.idx = None
#             item_doc.name = None

#             for row in locations:
#                 row.update({
#                     'picked_qty': row.stock_qty
#                 })

#                 location = item_doc.as_dict()
#                 location.update(row)
#                 self.append('locations', location)

#         # If table is empty on update after submit, set stock_qty, picked_qty to 0 so that indicator is red
#         # and give feedback to the user. This is to avoid empty Pick Lists.
#         if not self.get('locations') and self.docstatus == 1:
#             for location in locations_replica:
#                 location.stock_qty = 0
#                 location.picked_qty = 0
#                 self.append('locations', location)
#             frappe.msgprint(
#                 _("Please Restock Items and Update the Pick List to continue. To discontinue, cancel the Pick List."),
#                 title=_("Out of Stock"), indicator="red")

#         if save:
#             self.save()

# def get_available_item_locations(item_code, from_warehouses, required_qty, company, ignore_validation=False,item_doc = None):
#     locations = []
#     has_serial_no  = frappe.get_cached_value('Item', item_code, 'has_serial_no')
#     has_batch_no = frappe.get_cached_value('Item', item_code, 'has_batch_no')

#     if has_batch_no and has_serial_no:
#         locations = get_available_item_locations_for_serial_and_batched_item(item_code, from_warehouses, required_qty, company)
#     elif has_serial_no:
#         locations = get_available_item_locations_for_serialized_item(item_code, from_warehouses, required_qty, company)
#     elif has_batch_no:
#         locations = get_available_item_locations_for_batched_item(item_code, from_warehouses, required_qty, company,item_doc)
#     else:
#         locations = get_available_item_locations_for_other_item(item_code, from_warehouses, required_qty, company)

#     total_qty_available = sum(location.get('qty') for location in locations)

#     remaining_qty = required_qty - total_qty_available

#     if remaining_qty > 0 and not ignore_validation:
#         frappe.msgprint(_('{0} units of Item {1} is not available.')
#             .format(remaining_qty, frappe.get_desk_link('Item', item_code)),
#             title=_("Insufficient Stock"))

#     return locations


# def get_available_item_locations_for_batched_item(item_code, from_warehouses, required_qty, company,item_doc):
#     warehouse_condition = 'and warehouse in %(warehouses)s' if from_warehouses else ''
#     batch_locations = frappe.db.sql("""
#         SELECT
#             sle.`warehouse`,
#             sle.`batch_no`,
#             SUM(sle.`actual_qty`) AS `qty`
#         FROM
#             `tabStock Ledger Entry` sle, `tabBatch` batch
#         WHERE
#             sle.batch_no = batch.name
#             and sle.`item_code`=%(item_code)s
#             and sle.`company` = %(company)s
#             and batch.disabled = 0
#             and IFNULL(batch.`expiry_date`, '2200-01-01') > %(today)s
#             {warehouse_condition}
#         GROUP BY
#             `warehouse`,
#             `batch_no`,
#             `item_code`
#         HAVING `qty` > 0
#         ORDER BY IFNULL(batch.`expiry_date`, '2200-01-01'), batch.`creation`
#     """.format(warehouse_condition=warehouse_condition), { #nosec
#         'item_code': item_code,
#         'company': company,
#         'today': today(),
#         'warehouses': from_warehouses
#     }, as_dict=1)
#     if item_doc.sales_order_item:
#         result = frappe.db.sql("""select tcqi.name  
#                             from `tabSales Order Item` as tsoi
#                             inner join `tabCustomer Quality Inspection` as tcqi on tsoi.name = tcqi.sales_order_line
#                             where tsoi.name = %s and tcqi.docstatus = 1 limit 1""", (item_doc.sales_order_item))
#         if result:
#             lst = []
#             result1 = frappe.db.sql("""select
#                                 tcqi.sales_order_line,tcqi.item
#                                 ,tqip.specification  
#                                 from`tabCustomer Quality Inspection` as tcqi
#                                 inner join `tabItem Quality Inspection Parameter` as tqip on tqip.parent = tcqi.name
#                                 where tcqi.name = %s """, (result[0][0]), as_dict=True)
#             for s in result1:
#                 lst.append(s.specification)
#             if lst:
#                 batch_final_lst = []
#                 for batch in batch_locations:
#                     if batch:
#                         batch_insp_ln = frappe.get_all("Quality Inspection Reading", filters={"parent": ["=", batch.batch_no],
#                                                                                               "specification": ["in",
#                                                                                                                 lst]},
#                                                        fields=['name'])
#                         if batch_insp_ln:
#                             batch_i_ln = frappe.get_all("Quality Inspection Reading",
#                                                         filters={"parent": ["=", batch.batch_no],
#                                                                  "specification": ["in", lst], "status": "Rejected"},
#                                                         fields=['name'])
#                             if not batch_i_ln:
#                                 batch_final_lst.append(batch)
#                 return batch_final_lst
#             else:
#                 return batch_locations
#         else:
#             return batch_locations
#     return batch_locations
