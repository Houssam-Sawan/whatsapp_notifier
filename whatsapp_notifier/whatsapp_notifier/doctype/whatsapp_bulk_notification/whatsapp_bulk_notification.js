// Copyright (c) 2025, eng.houssam.sawan@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('WhatsApp Bulk Notification', {
    refresh: function(frm) {
        if (frm.doc.company) {
            frm.add_custom_button(__('Get Late Paying Customers'), function() {
                frappe.call({
                    method: 'whatsapp_notifier.whatsapp_notifier.doctype.whatsapp_bulk_notification.whatsapp_bulk_notification.get_late_paying_customers_details',
                    args: {
                        company: frm.doc.company
                    },
                    callback: function(r) {
                        if (r.message) {
                            frm.clear_table('customers');
                            r.message.forEach(d => {
                                let row = frm.add_child('customers', d);
                            });
                            frm.refresh_field('customers');
                            frappe.msgprint(__('Customer list updated.'));
                        }
                    }
                });
            });
        }
    },

    validate: function(frm) {
        (frm.doc.customers || []).forEach(row => {
            if (!row.mobile_number) {
                frappe.throw(__('Mobile number missing for customer: {0}', [row.customer_name]));
            }
        });
    },

    on_submit: function(frm) {
        (frm.doc.customers || []).forEach(row => {
            frappe.call({
                method: 'whatsapp_notifier.app.send_message',
                args: {
                    phone: row.mobile_number,
                    message: `Dear ${row.customer_name}, your credit limit is exceeded, Please clear it soon.
                    Credit Limit: ${row.credit_limit}
                    Outstanding Amount: ${row.outstanding_amount}
                    Remaining Credit: ${row.remaining_credit}
                    Thank you!`
                },
            });
        });
    }
});
