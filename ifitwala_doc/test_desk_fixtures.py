import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _load_json(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def test_crm_desktop_icon_points_to_workspace_sidebar():
	icon = _load_json(ROOT / "desktop_icon" / "ifitwala_crm.json")

	assert icon["doctype"] == "Desktop Icon"
	assert icon["hidden"] == 0
	assert icon["label"] == "Ifitwala CRM"
	assert icon["name"] == "Ifitwala CRM"
	assert icon["icon_type"] == "Link"
	assert icon["link_type"] == "Workspace Sidebar"
	assert icon["link_to"] == "Ifitwala CRM"


def test_crm_workspace_sidebar_home_points_to_crm_workspace():
	sidebar = _load_json(ROOT / "workspace_sidebar" / "ifitwala_crm.json")

	assert sidebar["doctype"] == "Workspace Sidebar"
	assert sidebar["name"] == "Ifitwala CRM"
	assert sidebar["title"] == "Ifitwala CRM"
	assert sidebar["items"][0]["label"] == "Home"
	assert sidebar["items"][0]["link_type"] == "URL"
	assert sidebar["items"][0]["url"] == "/desk/crm"
