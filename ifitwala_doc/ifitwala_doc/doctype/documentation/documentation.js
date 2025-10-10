// Copyright (c) 2025, François de Ryckel and contributors
// For license information, please see license.txt

frappe.ui.form.on('Documentation', {
  refresh(frm) {
    if (frm.is_new()) return;

    // Preview works for Draft or Published
    frm.add_custom_button('Preview', () => {
      const lang = frm.doc.language || 'en';
      const slug = frm.doc.slug;
      const url = `/docs/preview/${lang}/${slug}`;
      window.open(url, '_blank');
    }, 'Actions');

    // One-click rebuild (no token in browser; we call server-side helper)
    frm.add_custom_button('Rebuild Docs', async () => {
      try {
        await frappe.call('ifitwala_doc.api.build.kick_build');
        frappe.show_alert({ message: 'Docs rebuild queued', indicator: 'green' });
      } catch (e) {
        frappe.msgprint({ title: 'Rebuild failed', message: e?.message || String(e), indicator: 'red' });
      }
    }, 'Actions');

    // Publish/Unpublish toggles + rebuild
    if (frm.doc.status === 'Published') {
      frm.add_custom_button('Unpublish', () => toggle_status(frm, 'Draft'), 'Actions');
    } else {
      frm.add_custom_button('Publish', () => toggle_status(frm, 'Published'), 'Actions');
    }
  },

  title(frm) {
    if (!frm.doc.slug) {
      frm.set_value('slug', frappe.utils.slug(frm.doc.title));
    }
  }
});

async function toggle_status(frm, status) {
  frappe.confirm(`Set status to ${status}?`, async () => {
    await frm.set_value('status', status);
    await frm.save();
    try {
      await frappe.call('ifitwala_doc.api.build.kick_build');
      frappe.show_alert({ message: 'Updated & rebuild queued', indicator: 'green' });
    } catch (e) {
      frappe.msgprint({ title: 'Rebuild failed', message: e?.message || String(e), indicator: 'red' });
    }
  });
}
