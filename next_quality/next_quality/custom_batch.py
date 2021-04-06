from __future__ import unicode_literals
import frappe


def set_status(self,method):
    count = 0
    for i in self.test_result:
        if i.get('status') == "Rejected":
            count = count + 1
    if (count == 0):
        self.status = "Accepted"
    else:
        self.status = "Rejected"
