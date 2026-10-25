from __future__ import annotations

import importlib
import importlib.util
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HOOKS_PATH = REPO_ROOT / "erpnext_amazon_business_reconciliation" / "hooks.py"
SCHEDULER_SYNC_STUB = (
	"erpnext_amazon_business_reconciliation.amazon_business_reconciliation.tasks.sync.scheduled_sync_stub"
)


def _load_hooks():
	spec = importlib.util.spec_from_file_location("recon_hooks", HOOKS_PATH)
	module = importlib.util.module_from_spec(spec)
	assert spec.loader is not None
	spec.loader.exec_module(module)
	return module


def _resolve_hook(dotted_path: str):
	module_path, _, attr = dotted_path.rpartition(".")
	module = importlib.import_module(module_path)
	return getattr(module, attr)


class TestHooksContract(unittest.TestCase):
	def test_required_apps_include_core_amazon_business(self) -> None:
		hooks = _load_hooks()
		self.assertIn("erpnext", hooks.required_apps)
		self.assertIn("erpnext_amazon_business", hooks.required_apps)

	def test_scheduler_registers_sync_stub(self) -> None:
		hooks = _load_hooks()
		cron = hooks.scheduler_events.get("cron", {})
		paths = [entry for entries in cron.values() for entry in entries]
		self.assertIn(SCHEDULER_SYNC_STUB, paths)
		self.assertIsNone(_resolve_hook(SCHEDULER_SYNC_STUB)())


if __name__ == "__main__":
	unittest.main()
