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
    lead_owner=None,
    next_follow_up_on=None,
):
    lead = frappe.get_doc(
        {
            "doctype": "Lead",
            "first_name": first_name,
            "last_name": last_name,
            # Standard Lead integrations may read email_id; the custom doctype uses email.
            "email_id": email,
            "email": email,
            "phone": phone,
            "organization": organization,
            "organization_type": organization_type,
            "school_name": school_name,
            "job_title": job_title,
            "interest_area": interest_area,
            "current_system": current_system,
            "source": source,
            "notes": notes,
            "lead_owner": lead_owner,
            "next_follow_up_on": next_follow_up_on,
            "status": "New",
        }
    )
    lead.insert(ignore_permissions=True)
    return lead.name
