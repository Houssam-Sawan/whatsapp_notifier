# Copyright (c) 2025, eng.houssam.sawan@gmail.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class WhatsAppBulkNotification(Document):
	pass
import frappe
from prime.doc_events.sales_invoice import get_customer_financials

@frappe.whitelist()
def get_late_paying_customers_details(company):

    # get all customers (you can filter further if needed)
    customers = frappe.db.get_all('Customer', pluck='name')
    credit_details_list = []

    for customer in customers:
        try:            
            doc={"customer": customer}
            financials = get_customer_financials(doc, customer, company)
            if not financials or isinstance(financials, bool):
                    continue
            outstanding_amount = financials.get("outstanding_amount", 0)
            credit_limit = financials.get("credit_limit", 0)
            remaining_days = financials.get("credit_days", 0)
            remaining_credit = financials.get("remaining_credit", 0)
            owner_number_of_unpaid_invoices = financials.get("owner_number_of_unpaid_invoices", 0)

            if outstanding_amount > credit_limit*0.9:

                credit_details = {
                    "customer": customer,
                    "customer_name": customer["customer_name"],
                    "mobile_no": customer["mobile_no"],
                    "outstanding_amount": outstanding_amount,
                    "remaining_credit": remaining_credit,
                    "remaining_number_of_invoices": owner_number_of_unpaid_invoices,
                    "remaining_days": remaining_days
                }
                credit_details_list.append(credit_details)
        except Exception as e:
            frappe.log_error(f"Error processing {customer.name}: {e}")


    return credit_details_list
