
import frappe

@frappe.whitelist(allow_guest=True)
def capture_lead(first_name, email, last_name=None, phone=None, school_name=None, job_title=None, source="Website", notes=None):
    lead = frappe.get_doc({
        "doctype": "Lead",
        "first_name": first_name,
        "last_name": last_name,
        "email_id": email, # Standard field is email_id usually in Core, but since I created Custom Lead, use 'email'
        "email": email,    # I defined 'email' in my JSON
        "phone": phone,
        "school_name": school_name,
        "job_title": job_title,
        "source": source,
        "notes": notes,
        "status": "New"
    })
    lead.insert(ignore_permissions=True)
    return lead.name
