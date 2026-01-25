// Copyright (c) 2025, François de Ryckel and contributors
// For license information, please see license.txt

frappe.ui.form.on("Ifitwala Website Settings", {
	refresh(frm) {
		frm.add_custom_button(__("Deploy Website"), () => {
			frappe.call({
				method: "ifitwala_doc.api.build.kick_build",
				freeze: true,
				freeze_message: __("Starting build process..."),
				callback: function (r) {
					if (r.message && r.message.queued) {
						frappe.show_alert({
							message: __(r.message.message),
							indicator: "green"
						});
					}
				}
			});
		});

		frappe.realtime.on("astro_build_status", (data) => {
			if (data.status === "completed") {
				frappe.msgprint({
					title: __("Build Complete"),
					message: __(data.message),
					indicator: "green"
				});
			} else if (data.status === "failed") {
				frappe.msgprint({
					title: __("Build Failed"),
					message: __(data.message),
					indicator: "red"
				});
			}
		});
	},
});
