import frappe
from frappe import _
from frappe.model.document import Document


class AmazonBusinessPurchase(Document):
	"""P0 schema with idempotency validation; sync and PINV logic ships in P1."""

	def validate(self) -> None:
		if not (self.company and self.storefront and self.amazon_transaction_id):
			return
		filters = {
			"company": self.company,
			"storefront": self.storefront,
			"amazon_transaction_id": self.amazon_transaction_id,
		}
		if self.name:
			filters["name"] = ("!=", self.name)
		if frappe.db.exists("Amazon Business Purchase", filters):
			frappe.throw(
				_(
					"Amazon Business Purchase already exists for company {0}, storefront {1}, transaction {2}"
				).format(self.company, self.storefront, self.amazon_transaction_id),
				frappe.UniqueValidationError,
			)
