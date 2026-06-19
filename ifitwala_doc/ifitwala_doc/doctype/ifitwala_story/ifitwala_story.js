frappe.ui.form.on('Ifitwala Story', {
  refresh(frm) {
    if (frm.is_new()) return;

    if (frm.doc.status === 'Published' && frm.doc.slug) {
      frm.add_custom_button('View Story', () => {
        window.open(`/insights/${frm.doc.slug}/`, '_blank');
      }, 'Actions');
    }

    frm.add_custom_button('Rebuild Site', async () => {
      try {
        await frappe.call('ifitwala_doc.api.build.kick_build');
        frappe.show_alert({ message: 'Site rebuild queued', indicator: 'green' });
      } catch (e) {
        frappe.msgprint({ title: 'Rebuild failed', message: e?.message || String(e), indicator: 'red' });
      }
    }, 'Actions');

    if (frm.doc.status === 'Published') {
      frm.add_custom_button('Unpublish', () => toggle_status(frm, 'Draft'), 'Actions');
    } else {
      frm.add_custom_button('Publish', () => toggle_status(frm, 'Published'), 'Actions');
    }

    frappe.realtime.off('astro_build_status');
    frappe.realtime.on('astro_build_status', (data) => {
      if (data.status === 'completed') {
        frappe.show_alert({ message: data.message, indicator: 'green' });
      } else if (data.status === 'failed') {
        frappe.msgprint({ title: 'Build Failed', message: data.message, indicator: 'red' });
      }
    });
  },

  title(frm) {
    if (!frm.doc.slug && frm.doc.title) {
      frm.set_value('slug', frappe.utils.slug(frm.doc.title));
    }
  },
});

async function toggle_status(frm, status) {
  frappe.confirm(`Set status to ${status}?`, async () => {
    await frm.set_value('status', status);
    await frm.save();
    try {
      await frappe.call('ifitwala_doc.api.build.kick_build');
      frappe.show_alert({ message: 'Updated and rebuild queued', indicator: 'green' });
    } catch (e) {
      frappe.msgprint({ title: 'Rebuild failed', message: e?.message || String(e), indicator: 'red' });
    }
  });
}
