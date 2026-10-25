import frappe


def after_install() -> None:
	_ensure_reconciliation_settings_defaults()


def after_migrate() -> None:
	_ensure_reconciliation_settings_defaults()


def _ensure_reconciliation_settings_defaults() -> None:
	if not frappe.db.exists("DocType", "Amazon Business Reconciliation Settings"):
		return
	settings = frappe.get_single("Amazon Business Reconciliation Settings")
	changed = False
	if settings.enable_p1 is None:
		settings.enable_p1 = 1
		changed = True
	if settings.sync_lookback_days is None:
		settings.sync_lookback_days = 30
		changed = True
	if not settings.sync_schedule:
		settings.sync_schedule = "Daily"
		changed = True
	if settings.sync_cron_hour is None:
		settings.sync_cron_hour = 2
		changed = True
	if settings.document_poll_max_minutes is None:
		settings.document_poll_max_minutes = 15
		changed = True
	if settings.store_invoices_in_drive is None:
		settings.store_invoices_in_drive = 1
		changed = True
	if settings.drive_create_missing_folders is None:
		settings.drive_create_missing_folders = 1
		changed = True
	if changed:
		settings.save(ignore_permissions=True)
