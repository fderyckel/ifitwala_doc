// Copyright (c) 2025, François de Ryckel and contributors
// For license information, please see license.txt

frappe.ui.form.on('Documentation', {
  refresh(frm) {
    if (frm.is_new()) return;

    // ───────────────────────────────────────────────────────────
    // Existing Actions
    // ───────────────────────────────────────────────────────────
    frm.add_custom_button('Preview', () => {
      const lang = frm.doc.language || 'en';
      const slug = frm.doc.slug;
      const url = `/docs/preview/${lang}/${slug}`;
      window.open(url, '_blank');
    }, 'Actions');

    frm.add_custom_button('Rebuild Docs', async () => {
      try {
        const hasUnsavedChanges = typeof frm.is_dirty === 'function'
          ? frm.is_dirty()
          : Boolean(frm.doc.__unsaved);

        if (hasUnsavedChanges) {
          frappe.show_alert({ message: 'Saving changes before rebuild...', indicator: 'blue' });
          await frm.save();
        }

        if (frm.doc.status !== 'Published') {
          frappe.msgprint({
            title: 'Document is not published',
            message: 'This document was saved, but static docs only include Published records. Use Preview for drafts, or publish the document before rebuilding.',
            indicator: 'orange'
          });
          return;
        }

        await frappe.call('ifitwala_doc.api.build.kick_build');
        frappe.show_alert({ message: 'Docs rebuild queued', indicator: 'green' });
      } catch (e) {
        frappe.msgprint({ title: 'Rebuild failed', message: e?.message || String(e), indicator: 'red' });
      }
    }, 'Actions');

    if (frm.doc.status === 'Published') {
      frm.add_custom_button('Unpublish', () => toggle_status(frm, 'Draft'), 'Actions');
    } else {
      frm.add_custom_button('Publish', () => toggle_status(frm, 'Published'), 'Actions');
    }

    // ───────────────────────────────────────────────────────────
    // Screenshots grid toolbar (one-time bind)
    // ───────────────────────────────────────────────────────────
    // ───────────────────────────────────────────────────────────
    // Screenshots grid toolbar (one-time bind)
    // ───────────────────────────────────────────────────────────
    bind_screenshot_toolbar(frm);

    // ───────────────────────────────────────────────────────────
    // Realtime Feedback
    // ───────────────────────────────────────────────────────────
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
    // only auto-slug if slug is empty
    if (!frm.doc.slug && frm.doc.title) {
      frm.set_value('slug', frappe.utils.slug(frm.doc.title));
    }
  }
});

// ───────────────────────────────────────────────────────────────
// Helpers
// ───────────────────────────────────────────────────────────────
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

function bind_screenshot_toolbar(frm) {
  const grid = frm.fields_dict?.screenshots?.grid;
  if (!grid) return;
  if (grid.__ifw_bound) return;
  grid.__ifw_bound = true;

  // Add grid menu actions
  grid.add_custom_button && grid.add_custom_button('Copy Markdown (selected)', () => {
    const rows = grid.get_selected_children() || [];
    if (!rows.length) return frappe.show_alert({ message: 'No rows selected', indicator: 'orange' });
    rows.forEach(r => copy_markdown(r));
  });

  grid.add_custom_button && grid.add_custom_button('Copy Token (selected)', () => {
    const rows = grid.get_selected_children() || [];
    if (!rows.length) return frappe.show_alert({ message: 'No rows selected', indicator: 'orange' });
    rows.forEach(r => copy_token(r));
  });

  grid.add_custom_button && grid.add_custom_button('Queue Variants (selected)', async () => {
    const rows = grid.get_selected_children() || [];
    if (!rows.length) return frappe.show_alert({ message: 'No rows selected', indicator: 'orange' });

    // quick client validation first
    const issues = validate_screenshots_client(frm);
    if (issues.length) {
      frappe.msgprint({
        title: 'Fix these before queuing',
        message: `<ul>${issues.map(i => `<li>${frappe.utils.escape_html(i)}</li>`).join('')}</ul>`,
        indicator: 'red'
      });
      return;
    }

    const docname = frm.doc.name;
    let queued = 0, failed = 0;
    for (const r of rows) {
      try {
        await frappe.call({
          method: 'ifitwala_doc.ifitwala_doc.doctype.documentation.documentation._generate_row_variants',
          args: { docname, row_idx: r.idx }
        });
        queued++;
      } catch (e) {
        failed++;
      }
    }
    frappe.show_alert({ message: `Queued ${queued} row(s)${failed ? `, ${failed} failed` : ''}`, indicator: failed ? 'orange' : 'green' });
    // refresh to reflect generated_variants after workers run & save
    frm.reload_doc();
  });

  grid.add_custom_button && grid.add_custom_button('Validate Screenshots', () => {
    const issues = validate_screenshots_client(frm);
    if (issues.length) {
      frappe.msgprint({
        title: 'Screenshot Issues',
        message: `<ul>${issues.map(i => `<li>${frappe.utils.escape_html(i)}</li>`).join('')}</ul>`,
        indicator: 'red'
      });
    } else {
      frappe.show_alert({ message: 'Looks good ✨', indicator: 'green' });
    }
  });
}

// Build the user-facing snippets
function copy_markdown(r) {
  const size = (r.display_size || 'auto').trim();
  const fig  = (r.anchor_id || `fig-${r.idx}`).trim();
  const alt  = (r.alt_text || '').replace(/\n/g, ' ').trim() || 'screenshot';
  const md   = `![${alt}](docs://${fig}){data-size="${size}"}`;
  frappe.utils.copy_to_clipboard(md);
  frappe.show_alert({ message: `Copied Markdown for ${fig}`, indicator: 'green' });
}

function copy_token(r) {
  const size = (r.display_size || 'auto').trim();
  const fig  = (r.anchor_id || `fig-${r.idx}`).trim();
  const tk   = `[[fig:${fig} size=${size}]]`;
  frappe.utils.copy_to_clipboard(tk);
  frappe.show_alert({ message: `Copied token for ${fig}`, indicator: 'green' });
}

// Lightweight client-side validation to catch obvious issues early
function validate_screenshots_client(frm) {
  const issues = [];
  const rows = (frm.doc.screenshots || []);
  const seen = new Set();

  rows.forEach(r => {
    const anchor = (r.anchor_id || '').trim();
    if (!anchor) issues.push(`Row #${r.idx}: Anchor ID is required`);
    const key = anchor.toLowerCase();
    if (key) {
      if (seen.has(key)) issues.push(`Duplicate Anchor ID: ${anchor} (row #${r.idx})`);
      seen.add(key);
    }
    if (!r.image) issues.push(`Row #${r.idx}: Screenshot image is required`);
    if (!r.alt_text) issues.push(`Row #${r.idx}: Alt Text is required`);
    const size = (r.display_size || 'auto').trim().toLowerCase();
    if (!['auto','large','medium','small','thumb'].includes(size)) {
      issues.push(`Row #${r.idx}: Invalid display size "${r.display_size}"`);
    }
  });

  return issues;
}
