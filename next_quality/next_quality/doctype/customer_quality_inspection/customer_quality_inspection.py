# -*- coding: utf-8 -*-
# Copyright (c) 2021, Dexciss Technology Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CustomerQualityInspection(Document):
	@frappe.whitelist()
	def get_template_line(self):
		if self.quality_inspection_template:
			qit = frappe.get_doc("Quality Inspection Template",self.quality_inspection_template)
			lst =[]
			for res in qit.item_quality_inspection_parameter:
				lst.append(res.as_dict())
			return lst
		return False

