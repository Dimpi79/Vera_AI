from services.loader import DatasetLoader
from core.context_store import ContextStore
from core.decision_engine import DecisionEngine


loader = DatasetLoader()
loader.load_all()

store = ContextStore(loader)

engine = DecisionEngine()


context = store.build_context(

    merchant_id="m_001_drmeera_dentist_delhi",

    customer_id="c_001_priya_for_m001",

    trigger_id="trg_003_recall_due_priya"

)

decision = engine.decide(context)

print("\n========== DECISION ==========\n")

for key, value in decision.items():
    print(f"{key:15}: {value}")