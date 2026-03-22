
import frappe


@frappe.whitelist(allow_guest=True)
def capture_lead(
    first_name,
    email,
    last_name=None,
    phone=None,
    organization=None,
    organization_type=None,
    school_name=None,
    job_title=None,
    interest_area=None,
    current_system=None,
    source="Website",
    notes=None,
):
    lead = frappe.get_doc({
        "doctype": "Lead",
        "first_name": first_name,
        "last_name": last_name,
        "email_id": email, # Standard field is email_id usually in Core, but since I created Custom Lead, use 'email'
        "email": email,    # I defined 'email' in my JSON
        "phone": phone,
        "organization": organization,
        "organization_type": organization_type,
        "school_name": school_name,
        "job_title": job_title,
        "interest_area": interest_area,
        "current_system": current_system,
        "source": source,
        "notes": notes,
        "status": "New"
    })
    lead.insert(ignore_permissions=True)
    return lead.name
