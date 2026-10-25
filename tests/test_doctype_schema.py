from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCTYPE_DIR = (
	REPO_ROOT / "erpnext_amazon_business_reconciliation" / "amazon_business_reconciliation" / "doctype"
)

EXPECTED_DOCTYPES = {
	"Amazon Business Reconciliation Settings",
	"Amazon Business Company Books Config",
	"Amazon Business Storefront Sync State",
	"Amazon Business Purchase",
	"Amazon Business Purchase Item",
	"Amazon Business Purchase Shipment",
	"Amazon Business Sync Log",
	"Amazon Business Reconciliation Log",
}

CHILD_TABLES = {
	"Amazon Business Purchase Item",
	"Amazon Business Purchase Shipment",
}


def _load_doctype_json(path: Path) -> dict:
	with path.open(encoding="utf-8") as handle:
		return json.load(handle)


class TestDocTypeSchema(unittest.TestCase):
	def test_all_p0_doctypes_present(self) -> None:
		found = set()
		for folder in DOCTYPE_DIR.iterdir():
			if not folder.is_dir():
				continue
			for json_path in folder.glob("*.json"):
				doc = _load_doctype_json(json_path)
				self.assertEqual(doc.get("doctype"), "DocType")
				found.add(doc.get("name"))
		self.assertEqual(found, EXPECTED_DOCTYPES)

	def test_reconciliation_settings_is_single(self) -> None:
		path = (
			DOCTYPE_DIR
			/ "amazon_business_reconciliation_settings"
			/ "amazon_business_reconciliation_settings.json"
		)
		doc = _load_doctype_json(path)
		self.assertEqual(doc.get("issingle"), 1)

	def test_child_tables_and_purchase_links(self) -> None:
		for name in CHILD_TABLES:
			slug = name.lower().replace(" ", "_")
			doc = _load_doctype_json(DOCTYPE_DIR / slug / f"{slug}.json")
			self.assertEqual(doc.get("istable"), 1)

		purchase = _load_doctype_json(
			DOCTYPE_DIR / "amazon_business_purchase" / "amazon_business_purchase.json"
		)
		table_fields = {
			field["fieldname"]: field.get("options")
			for field in purchase["fields"]
			if field.get("fieldtype") == "Table"
		}
		self.assertEqual(table_fields.get("items"), "Amazon Business Purchase Item")
		self.assertEqual(table_fields.get("shipments"), "Amazon Business Purchase Shipment")

	def test_unique_indexes_for_idempotency(self) -> None:
		purchase = _load_doctype_json(
			DOCTYPE_DIR / "amazon_business_purchase" / "amazon_business_purchase.json"
		)
		purchase_index_fields = {tuple(index["fields"]) for index in purchase.get("indexes", [])}
		self.assertIn(("company", "storefront", "amazon_transaction_id"), purchase_index_fields)

		sync_state = _load_doctype_json(
			DOCTYPE_DIR
			/ "amazon_business_storefront_sync_state"
			/ "amazon_business_storefront_sync_state.json"
		)
		sync_index_fields = {tuple(index["fields"]) for index in sync_state.get("indexes", [])}
		self.assertIn(("company", "storefront"), sync_index_fields)


if __name__ == "__main__":
	unittest.main()
