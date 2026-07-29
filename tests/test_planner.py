import unittest

from core.planner import Planner


class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.planner = Planner()

    def test_selects_high_value_facts_and_deduplicates(self):
        context = {
            "merchant": {},
            "customer": {},
            "trigger": {
                "kind": "perf_dip",
                "payload": {
                    "topic": "dentist",
                    "offer": "20% off",
                    "lead": "urgent"
                }
            }
        }
        decision = {
            "audience": "merchant",
            "intent": "inform",
            "goal": "increase appointments",
            "priority": "high",
            "strategy": "promote"
        }
        evidence = {
            "merchant_name": "Asha",
            "owner_name": "Asha",
            "customer_name": "Priya",
            "category_slug": "dentists",
            "has_active_offer": True,
            "merchant_engaged": True,
            "trigger_payload": {
                "topic": "dentist",
                "offer": "20% off"
            },
            "performance": {"views": 120, "ctr": 0.8},
            "offers": [{"price": 499}]
        }

        plan = self.planner.build_plan(context, decision, evidence)
        facts = plan["facts"]

        self.assertLessEqual(len(facts), 3)
        self.assertTrue(any("offer" in fact.lower() for fact in facts))
        self.assertTrue(any("visit" in fact.lower() or "response" in fact.lower() for fact in facts))
        self.assertFalse(any("recently interacted" in fact.lower() for fact in facts))


if __name__ == "__main__":
    unittest.main()
