import frappe
from frappe import _
from frappe.model.document import Document


class AmazonBusinessStorefrontSyncState(Document):
	"""P0 schema with idempotency validation; sync and PINV logic ships in P1."""

	def validate(self) -> None:
		if not (self.company and self.storefront):
			return
		filters = {"company": self.company, "storefront": self.storefront}
		if self.name:
			filters["name"] = ("!=", self.name)
		if frappe.db.exists("Amazon Business Storefront Sync State", filters):
			frappe.throw(
				_("Storefront Sync State already exists for company {0} and storefront {1}").format(
					self.company, self.storefront
				),
				frappe.UniqueValidationError,
			)
