import frappe

ICON_NAME = "Ifitwala CRM"
EXPECTED_LINK_TYPE = "Workspace Sidebar"


def execute():
	if not frappe.db.exists("Desktop Icon", ICON_NAME):
		return

	icon = frappe.db.get_value(
		"Desktop Icon",
		ICON_NAME,
		["app", "link_type", "link_to", "icon_type"],
		as_dict=True,
	)
	if not icon or icon.get("app") != "ifitwala_doc":
		return

	updates = {}

	if icon.get("link_type") != EXPECTED_LINK_TYPE:
		updates["link_type"] = EXPECTED_LINK_TYPE

	if icon.get("link_to") != ICON_NAME:
		updates["link_to"] = ICON_NAME

	if icon.get("icon_type") != "Link":
		updates["icon_type"] = "Link"

	if not updates:
		return

	frappe.db.set_value("Desktop Icon", ICON_NAME, updates, update_modified=False)
	clear_desk_icon_cache()


def clear_desk_icon_cache():
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
