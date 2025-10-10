// Copyright (c) 2025, François de Ryckel and contributors
// For license information, please see license.txt

frappe.ui.form.on('Documentation', {
refresh(frm){
if(!frm.is_new()){
frm.add_custom_button('Preview', () => {
const url = `/docs/preview/${frm.doc.language || 'en'}/${frm.doc.slug}`
window.open(url, '_blank')
},'Actions')


if(frm.doc.status === 'Published'){
frm.add_custom_button('Unpublish', () => toggle_status(frm,'Draft'),'Actions')
} else {
frm.add_custom_button('Publish', () => toggle_status(frm,'Published'),'Actions')
}
}
},
title(frm){
if(!frm.doc.slug){
frm.set_value('slug', frappe.utils.slug(frm.doc.title))
}
}
})


function toggle_status(frm, status){
frappe.confirm(`Set status to ${status}?`, () => {
frm.set_value('status', status)
frm.save()
.then(() => frappe.call('ifitwala_ed.api.docs.on_publish_webhook', { name: frm.doc.name }))
.then(() => frappe.show_alert({message:'Updated & webhook sent', indicator:'green'}))
})
}
