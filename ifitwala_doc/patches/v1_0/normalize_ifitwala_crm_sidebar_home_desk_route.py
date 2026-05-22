import frappe

SIDEBAR_NAME = "Ifitwala CRM"
HOME_URL = "/desk/crm"


def execute():
	if not frappe.db.exists("Workspace Sidebar", SIDEBAR_NAME):
		return

	sidebar = frappe.get_doc("Workspace Sidebar", SIDEBAR_NAME)
	home_item = next((item for item in sidebar.items if item.label == "Home"), None)
	if not home_item:
		return

	changed = False

	if home_item.link_type != "URL":
		home_item.link_type = "URL"
		changed = True

	if getattr(home_item, "url", None) != HOME_URL:
		home_item.url = HOME_URL
		changed = True

	if getattr(home_item, "link_to", None):
		home_item.link_to = None
		changed = True

	if not changed:
		return

	sidebar.save(ignore_permissions=True)
	clear_desk_cache()


def clear_desk_cache():
	cache_factory = getattr(frappe, "cache", None)
	if not callable(cache_factory):
		return

	try:
		cache = cache_factory()
	except Exception:
		return

	if not cache or not hasattr(cache, "delete_key"):
		return

	cache.delete_key("desktop_icons")
	cache.delete_key("bootinfo")
