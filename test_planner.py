from services.loader import DatasetLoader
from core.context_store import ContextStore
from core.decision_engine import DecisionEngine
from core.evidence import EvidenceCollector
from core.planner import Planner

loader = DatasetLoader()
loader.load_all()

store = ContextStore(loader)
engine = DecisionEngine()
collector = EvidenceCollector()
planner = Planner()

context = store.build_context(
    merchant_id="m_001_drmeera_dentist_delhi",
    customer_id="c_001_priya_for_m001",
    trigger_id="trg_003_recall_due_priya"
)

decision = engine.decide(context)
evidence = collector.collect(context, decision)

plan = planner.build_plan(context, decision, evidence)

print("\n========== PLAN ==========\n")

for key, value in plan.items():
    print(f"{key}:")
    print(value)
    print()