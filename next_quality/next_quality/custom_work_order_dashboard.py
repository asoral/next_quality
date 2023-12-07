from __future__ import unicode_literals
from frappe import _

def get_data(data):
	return {
		'fieldname': 'work_order',
		'non_standard_fieldnames': {
		   'Quality Inspection': 'reference_name'
	    },
		'transactions': [
			{
				'label': _('Transactions'),
				'items': ['Stock Entry', 'Job Card', 'Pick List']
			},
			{
				'label': _('Inspection'),
				'items': ['Quality Inspection']
			},
		]
	}
