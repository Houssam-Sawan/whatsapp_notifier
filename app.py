import frappe
from frappe_twilio_integration.api import send_whatsapp

@frappe.whitelist()
def send_whatsapp_message(to, message):
    """
    Send WhatsApp message using Twilio Integration.
    Callable from Server Script or Client Script.
    """
    if not to or not message:
        frappe.throw("Phone number and message are required")

    # Normalize number
    number = ''.join([c for c in to if c.isdigit()])
    if not number.startswith("+"):
        number = f"+{number}"

    try:
        send_whatsapp(number, message)
        return f"Message sent successfully to {number}"
    except Exception as e:
        frappe.log_error(f"WhatsApp Error: {e}", "WhatsApp Notifier")
        frappe.throw(f"Failed to send message: {str(e)}")
