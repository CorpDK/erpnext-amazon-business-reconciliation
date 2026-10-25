# erpnext-amazon-business-reconciliation

Frappe v16 app **`erpnext_amazon_business_reconciliation`**: Amazon Business purchase register, draft Purchase Invoice creation, and desk reconciliation for ERPNext.

**Requires:** [`erpnext_amazon_business`](https://github.com/CorpDK/erpnext-amazon-business) (OAuth, storefront master, tokens on core Company Storefront rows). This app does not store LWA credentials.

## P0 scope (schema)

- Reconciliation Settings, Company Books Config, Storefront Sync State
- Amazon Business Purchase (+ line + shipment child tables)
- Sync Log and Reconciliation Log
- Desk workspace **Amazon Business Reconciliation**
- Scheduler hook stub (P1 implements sync)

## Install (bench)

```bash
bench get-app https://github.com/CorpDK/erpnext-amazon-business-reconciliation
bench --site <site> install-app erpnext_amazon_business_reconciliation
```

Install **erpnext_amazon_business** first.

## License

GPL-3.0-or-later — see [LICENSE](LICENSE).
