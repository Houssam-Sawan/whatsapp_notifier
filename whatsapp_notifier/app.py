import frappe
from twilio_integration.twilio_integration.doctype.whatsapp_message.whatsapp_message import WhatsAppMessage

@frappe.whitelist()
def send_whatsapp(to, message):
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
    numbers = [number]

    doctype = None
    docname = None
    try:
        WhatsAppMessage.send_whatsapp_message(numbers, message, doctype, docname)
        return f"Message sent successfully to {number}"
    except Exception as e:
        #frappe.log_error(f"WhatsApp Error: {e}", "WhatsApp Notifier")
        frappe.throw(f"Failed to send message: {str(e)}")


@frappe.whitelist()
def test_method(name):
    return f"hello {name}"

@frappe.whitelist()
def test_method_noargs():
    return f"hello No args"


