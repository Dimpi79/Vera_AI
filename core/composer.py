from core.decision_engine import DecisionEngine
from core.evidence import EvidenceCollector
from core.planner import Planner
from core.prompt_builder import PromptBuilder
from core.message_generator import MessageGenerator


class Composer:
    """
    Main orchestration class.

    Converts category + merchant + trigger + customer
    into one deterministic action.
    """

    def __init__(self):

        self.decision_engine = DecisionEngine()
        self.evidence_collector = EvidenceCollector()
        self.planner = Planner()
        self.prompt_builder = PromptBuilder()
        self.generator = MessageGenerator()

    def compose(self, context):

        # STEP 1: Extract structured evidence first
        evidence = self.evidence_collector.collect(
        context,
        {}
        )

        # Make evidence available to downstream components
        context["evidence"] = evidence

        # STEP 2: Make decision using evidence
        decision = self.decision_engine.decide(context)

        if not decision["should_send"]:
           return None

        # STEP 3: Build communication plan
        plan = self.planner.build_plan(
        context,
        decision,
        evidence
        )

        # Reserved for future LLM versions
        _ = self.prompt_builder.build(plan)

        # STEP 4: Generate final message
        body = self.generator.generate(plan)

        customer = context.get("customer")
        trigger = context["trigger"]
        merchant = context["merchant"]

        return {
        "merchant_id": merchant["merchant_id"],
        "trigger_id": trigger["id"],
        "customer_id": (
            customer["customer_id"]
            if customer else None
        ),
        "body": body,
        "cta": plan["cta"],
        "send_as": "vera",
        "suppression_key": (
            f"{merchant['merchant_id']}:{trigger['id']}"
        ),
        "rationale": decision["goal"]
    }