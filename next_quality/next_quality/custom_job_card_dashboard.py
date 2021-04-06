from __future__ import unicode_literals
from frappe import _

def get_data(data):
	return {
		'fieldname': 'job_card',
		'non_standard_fieldnames': {
			'InProcess Quality Inspection': 'reference_name'
		},
		'transactions': [
			{
				'label': _('Material'),
				'items': ['Material Consumption']
			},
			{
				'label': _('Transactions'),
				'items': ['InProcess Quality Inspection']
			}
		]
	}