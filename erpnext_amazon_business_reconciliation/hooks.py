app_name = "erpnext_amazon_business_reconciliation"
app_title = "Amazon Business Reconciliation"
app_publisher = "CorpDK"
app_description = "Amazon Business purchase register, PINV, and reconciliation for ERPNext"
app_email = "ops@corpdk.local"
app_license = "GPL-3.0-or-later"

required_apps = ["erpnext", "erpnext_amazon_business"]

add_to_apps_screen = [
	{
		"name": app_name,
		"title": app_title,
		"route": "/app/amazon-business-reconciliation",
		"has_permission": "erpnext_amazon_business_reconciliation.permissions.has_app_permission",
	},
]

before_install = "erpnext_amazon_business_reconciliation.patches.check_version_compatibility.execute"
before_migrate = "erpnext_amazon_business_reconciliation.patches.check_version_compatibility.execute"

after_install = "erpnext_amazon_business_reconciliation.install.after_install"
after_migrate = "erpnext_amazon_business_reconciliation.install.after_migrate"

# P0: reserved export filters; P1 adds Purchase Invoice / Item custom fields via fixtures.
fixtures = [
	{
		"dt": "Custom Field",
		"filters": [["name", "in", []]],
	},
]

scheduler_events = {
	"cron": {
		"0 2 * * *": [
			"erpnext_amazon_business_reconciliation.amazon_business_reconciliation.tasks.sync.scheduled_sync_stub",
		],
	},
}
