from __future__ import unicode_literals
from frappe import _

def get_data(data):
	return {
		'fieldname': 'purchase_receipt_no',
		'non_standard_fieldnames': {
			'Purchase Invoice': 'purchase_receipt',
			'Asset': 'purchase_receipt',
			'Landed Cost Voucher': 'receipt_document',
			'Auto Repeat': 'reference_document',
			'Purchase Receipt': 'return_against',
			'Quality Inspection':'reference_name'
		},
		'internal_links': {
			'Purchase Order': ['items', 'purchase_order'],
			'Project': ['items', 'project'],
			'Delivery Note':'inter_company_reference'
			
		},
		'transactions': [
			{
				'label': _('Related'),
				'items': ['Purchase Invoice', 'Landed Cost Voucher', 'Asset']
			},
			{
				'label': _('Reference'),
				'items': ['Purchase Order','Quality Inspection', 'Project','Delivery Note']
			},
			{
				'label': _('Returns'),
				'items': ['Purchase Receipt']
			},
			{
				'label': _('Subscription'),
				'items': ['Auto Repeat']
			},
			
		]
	}