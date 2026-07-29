import json
from pathlib import Path
from typing import Dict, List, Any


class DatasetLoader:
    """
    Loads all dataset files into memory.

    This class acts like an in-memory database so the rest of the
    project never needs to read JSON files directly.
    """

    def __init__(self, dataset_path: str = "dataset"):
        self.dataset_path = Path(dataset_path)

        # Complete datasets
        self.categories: Dict[str, Any] = {}
        self.merchants: List[Dict] = []
        self.customers: List[Dict] = []
        self.triggers: List[Dict] = []

        # Fast lookup dictionaries
        self.merchants_by_id: Dict[str, Dict] = {}
        self.customers_by_id: Dict[str, Dict] = {}
        self.triggers_by_id: Dict[str, Dict] = {}

    # --------------------------------------------------
    # Generic JSON Loader
    # --------------------------------------------------

    def _load_json(self, filepath: Path):
        print(f"Loading: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    # --------------------------------------------------
    # Categories
    # --------------------------------------------------

    def load_categories(self):

        category_folder = self.dataset_path / "categories"

        for file in category_folder.glob("*.json"):
            self.categories[file.stem] = self._load_json(file)

    # --------------------------------------------------
    # Merchants
    # --------------------------------------------------

    def load_merchants(self):

        file = self.dataset_path / "merchants_seed.json"

        data = self._load_json(file)

        self.merchants = data["merchants"]

        self.merchants_by_id = {
            merchant["merchant_id"]: merchant
            for merchant in self.merchants
        }

    # --------------------------------------------------
    # Customers
    # --------------------------------------------------

    def load_customers(self):

        file = self.dataset_path / "customers_seed.json"

        data = self._load_json(file)

        self.customers = data["customers"]

        self.customers_by_id = {
            customer["customer_id"]: customer
            for customer in self.customers
        }

    # --------------------------------------------------
    # Triggers
    # --------------------------------------------------

    def load_triggers(self):

        file = self.dataset_path / "triggers_seed.json"

        data = self._load_json(file)

        self.triggers = data["triggers"]

        # Trigger ID field is "id"
        self.triggers_by_id = {
            trigger["id"]: trigger
            for trigger in self.triggers
        }

    # --------------------------------------------------
    # Load Everything
    # --------------------------------------------------

    def load_all(self):

        self.load_categories()
        self.load_merchants()
        self.load_customers()
        self.load_triggers()

        print("\n✓ Dataset loaded successfully!")

    # --------------------------------------------------
    # Getter Methods
    # --------------------------------------------------

    def get_category(self, slug):
        return self.categories.get(slug)

    def get_merchant(self, merchant_id):
        return self.merchants_by_id.get(merchant_id)

    def get_customer(self, customer_id):
        return self.customers_by_id.get(customer_id)

    def get_trigger(self, trigger_id):
        return self.triggers_by_id.get(trigger_id)