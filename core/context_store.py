from services.loader import DatasetLoader


class ContextStore:
    """
    Builds a unified context object from dataset IDs.

    Every downstream module works with this context instead
    of querying the dataset repeatedly.
    """

    def __init__(self, loader: DatasetLoader):
        self.loader = loader

    def build_context(
        self,
        merchant_id: str,
        customer_id: str | None = None,
        trigger_id: str | None = None,
    ):

        merchant = self.loader.get_merchant(merchant_id)

        if merchant is None:
            raise ValueError(f"Merchant not found: {merchant_id}")

        customer = None
        if customer_id:
            customer = self.loader.get_customer(customer_id)
             
        trigger = None
        if trigger_id:
            trigger = self.loader.get_trigger(trigger_id)

        category_slug = merchant["category_slug"]
        category = self.loader.get_category(category_slug)

        return {
            "merchant": merchant,
            "customer": customer,
            "trigger": trigger,
            "category": category,
        }
        