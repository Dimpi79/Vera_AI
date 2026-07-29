from services.loader import DatasetLoader
from core.context_store import ContextStore

loader = DatasetLoader()
loader.load_all()

store = ContextStore(loader)

context = store.build_context(
    merchant_id="m_001_drmeera_dentist_delhi",
    customer_id="c_001_priya_for_m001",
    trigger_id="trg_003_recall_due_priya"
)

print("\n========== CONTEXT ==========")

print("Merchant :", context["merchant"]["identity"]["name"])
print("Customer :", context["customer"]["identity"]["name"])
print("Trigger  :", context["trigger"]["kind"])
print("Category :", context["merchant"]["category_slug"])
print(context["customer"])