from services.loader import DatasetLoader
from core.context_store import ContextStore
from core.decision_engine import DecisionEngine
from core.evidence import EvidenceCollector
from core.opportunity_scorer import OpportunityScorer


loader = DatasetLoader()
loader.load_all()

store = ContextStore(loader)
engine = DecisionEngine()
collector = EvidenceCollector()
scorer = OpportunityScorer()


context = store.build_context(
    merchant_id="m_001_drmeera_dentist_delhi",
    customer_id="c_001_priya_for_m001",
    trigger_id="trg_003_recall_due_priya"
)

decision = engine.decide(context)

evidence = collector.collect(context, decision)

result = scorer.score(evidence)

print("\n========== OPPORTUNITY ==========\n")

for k, v in result.items():
    print(f"{k:10}: {v}")