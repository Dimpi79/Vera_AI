from typing import Dict, Any


class EvidenceCollector:
    """
    Extracts structured evidence from the four contexts.

    The goal is to convert raw JSON into meaningful facts that the
    DecisionEngine can reason over.
    """

    def collect(self, context: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:

        merchant = context.get("merchant") or {}
        customer = context.get("customer") or {}
        category = context.get("category") or {}
        trigger = context.get("trigger") or {}

        evidence = {}

        # ---------------------------
        # Merchant Evidence
        # ---------------------------

        identity = merchant.get("identity", {})
        performance = merchant.get("performance", {})
        aggregate = merchant.get("customer_aggregate", {})

        evidence["merchant_name"] = identity.get("name")
        evidence["owner_name"] = identity.get("owner_first_name")
        evidence["city"] = identity.get("city")
        evidence["locality"] = identity.get("locality")

        evidence["verified"] = identity.get("verified", False)

        evidence["signals"] = merchant.get("signals", [])

        evidence["offers"] = [
            offer
            for offer in merchant.get("offers", [])
            if offer.get("status") == "active"
        ]

        evidence["has_active_offer"] = len(evidence["offers"]) > 0

        evidence["review_themes"] = merchant.get("review_themes", [])

        evidence["conversation_history"] = merchant.get(
            "conversation_history",
            []
        )

        evidence["merchant_engaged"] = any(
            item.get("engagement", "").startswith("merchant")
            or item.get("engagement", "").startswith("intent")
            for item in evidence["conversation_history"]
        )

        evidence["performance"] = performance

        evidence["customer_aggregate"] = aggregate

        # ---------------------------
        # Customer Evidence
        # ---------------------------

        if customer:

            identity = customer.get("identity", {})
            relationship = customer.get("relationship", {})
            preferences = customer.get("preferences", {})

            evidence["customer_name"] = identity.get("name")
            evidence["language"] = identity.get("language_pref")
            evidence["age_band"] = identity.get("age_band")

            evidence["customer_state"] = customer.get("state")

            evidence["lifetime_value"] = relationship.get(
                "lifetime_value",
                0
            )

            value = evidence["lifetime_value"]

            if value >= 10000:
                bucket = "vip"
            elif value >= 5000:
                bucket = "high"
            elif value >= 1500:
                bucket = "medium"
            else:
                bucket = "low"

            evidence["value_bucket"] = bucket

            evidence["preferred_slot"] = preferences.get(
                "preferred_slots"
            )

            evidence["channel"] = preferences.get("channel")

            evidence["preferences"] = preferences

            evidence["relationship"] = relationship

        else:

            evidence["customer_name"] = None
            evidence["customer_state"] = None
            evidence["value_bucket"] = None
            evidence["language"] = None

        # ---------------------------
        # Trigger Evidence
        # ---------------------------

        evidence["trigger_kind"] = trigger.get("kind")
        evidence["trigger_scope"] = trigger.get("scope")
        evidence["trigger_source"] = trigger.get("source")
        evidence["urgency"] = trigger.get("urgency", 1)
        evidence["expires_at"] = trigger.get("expires_at")
        evidence["trigger_payload"] = trigger.get("payload", {})

        # ---------------------------
        # Category Evidence
        # ---------------------------

        evidence["category_slug"] = category.get("slug")

        voice = category.get("voice", {})

        evidence["tone"] = voice.get("tone")

        evidence["offer_catalog"] = category.get(
            "offer_catalog",
            []
        )

        evidence["digest"] = category.get(
            "digest",
            []
        )

        evidence["peer_stats"] = category.get(
            "peer_stats",
            {}
        )

        evidence["seasonal_beats"] = category.get(
            "seasonal_beats",
            []
        )

        evidence["trend_signals"] = category.get(
            "trend_signals",
            []
        )

        # ---------------------------
        # Derived Evidence
        # ---------------------------

        evidence["facts"] = []

        if evidence["has_active_offer"]:
            evidence["facts"].append("merchant_has_active_offer")

        if evidence["merchant_engaged"]:
            evidence["facts"].append("merchant_recently_engaged")

        if evidence["customer_state"]:
            evidence["facts"].append(
                f"customer_{evidence['customer_state']}"
            )

        if evidence["verified"]:
            evidence["facts"].append("verified_business")

        if evidence["urgency"] >= 4:
            evidence["facts"].append("high_urgency_trigger")

        if evidence["digest"]:
            evidence["facts"].append("category_has_digest")

        return evidence