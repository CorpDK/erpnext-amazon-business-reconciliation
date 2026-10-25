from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SYNC_PATH = (
	REPO_ROOT
	/ "erpnext_amazon_business_reconciliation"
	/ "amazon_business_reconciliation"
	/ "tasks"
	/ "sync.py"
)


class TestSyncStub(unittest.TestCase):
	def test_scheduled_sync_stub_is_no_op(self) -> None:
		spec = importlib.util.spec_from_file_location("recon_sync", SYNC_PATH)
		module = importlib.util.module_from_spec(spec)
		assert spec.loader is not None
		spec.loader.exec_module(module)
		self.assertIsNone(module.scheduled_sync_stub())


if __name__ == "__main__":
	unittest.main()
