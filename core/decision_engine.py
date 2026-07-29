from typing import Dict


class DecisionEngine:
    """
    Converts context into a structured business decision.

    It DOES NOT generate the final message.
    It only decides:
      - who to talk to
      - why
      - how important it is
      - which strategy to use
      - what Vera wants to achieve
    """

    PRIORITY_MAP = {
        1: "low",
        2: "low",
        3: "medium",
        4: "high",
        5: "critical"
    }

    TRIGGER_RULES = {

        "recall_due": {
            "intent": "appointment_reminder",
            "audience": "customer",
            "goal": "Encourage customer to book a recall appointment."
        },

        "research_digest": {
            "intent": "merchant_insight",
            "audience": "merchant",
            "goal": "Share useful industry research."
        },

        "regulation_change": {
            "intent": "compliance_alert",
            "audience": "merchant",
            "goal": "Inform merchant about important regulation updates."
        },

        "perf_dip": {
            "intent": "performance_improvement",
            "audience": "merchant",
            "goal": "Help merchant improve business performance."
        },

        "renewal_due": {
            "intent": "renewal_reminder",
            "audience": "merchant",
            "goal": "Remind merchant about upcoming renewal."
        },

        "festival_upcoming": {
            "intent": "campaign_suggestion",
            "audience": "merchant",
            "goal": "Suggest a marketing campaign."
        }
    }

    STRATEGY_MAP = {
        "research_digest": "educate",
        "perf_dip": "coach",
        "festival_upcoming": "promote",
        "renewal_due": "retain",
        "recall_due": "convert",
        "regulation_change": "inform"
    }

    def decide(self, context: Dict):

        trigger = context.get("trigger")

        if trigger is None:
            raise ValueError("Trigger is required.")

        kind = trigger.get("kind")

        rule = self.TRIGGER_RULES.get(kind)

        if rule is None:
            return {
                "intent": "generic_update",
                "audience": trigger.get("scope", "merchant"),
                "priority": "medium",
                "should_send": False,
                "goal": "No matching business rule.",
                "reason": [f"unknown_trigger:{kind}"],
                "strategy": "observe",
                "cta_style": "none",
                "evidence": []
            }

        priority = self.PRIORITY_MAP.get(
            trigger.get("urgency", 3),
            "medium"
        )

        evidence = context.get("evidence", {})

        reasons = [kind]

        if evidence.get("merchant_engaged"):
            reasons.append("merchant_recently_engaged")

        if evidence.get("has_active_offer"):
            reasons.append("active_offer_available")

        if evidence.get("verified"):
            reasons.append("verified_business")

        if evidence.get("value_bucket") == "vip":
            reasons.append("vip_customer")

        strategy = self.STRATEGY_MAP.get(kind, "inform")

        cta_style = "direct"

        if evidence.get("merchant_engaged"):
            cta_style = "collaborative"

        if priority == "critical":
            cta_style = "urgent"

        return {

            "intent": rule["intent"],

            "audience": rule["audience"],

            "priority": priority,

            "should_send": True,

            "goal": rule["goal"],

            "strategy": strategy,

            "cta_style": cta_style,

            "reason": reasons,

            "evidence": evidence.get("facts", [])
        }