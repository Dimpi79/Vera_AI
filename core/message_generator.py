from typing import Dict, List, Tuple


class MessageGenerator:
    """
    Builds a concise, conversational message from the communication plan.
    It selects a few high-value facts, explains why they matter, and ends
    with one clear call to action.
    """

    def generate(self, plan: Dict) -> str:
        merchant = (
            plan.get("owner_name")
            or plan.get("merchant_name")
            or "there"
        )

        lines = [f"Hi {merchant},"]

        summary = plan.get("summary")
        if summary:
            lines.append(f"\n{summary}")

        evidence = plan.get("evidence", {})
        facts = self._select_facts(evidence, plan)

        for sentence in facts:
            lines.append(sentence)

        cta = plan.get("cta") or "Take action"
        lines.append(f"\n{cta}.")

        message = " ".join(lines)
        return self._enforce_limits(message)

    def _select_facts(self, evidence: Dict, plan: Dict) -> List[str]:
        selected: List[Tuple[str, str]] = []
        trigger_payload = evidence.get("trigger_payload", {})
        performance = evidence.get("performance", {})
        offers = evidence.get("offers") or []

        if evidence.get("has_active_offer") and offers:
            offer = offers[0]
            price = (
                offer.get("price")
                or offer.get("offer_price")
                or offer.get("discount_price")
            )
            if price:
                selected.append((
                    f"You already have an active offer at ₹{price}.",
                    "That gives you a ready promotion to use now."
                ))

        if performance.get("views"):
            selected.append((
                f"Your listing recently attracted {performance['views']} visits.",
                "That suggests there is still demand to capture."
            ))

        if performance.get("ctr") is not None:
            selected.append((
                f"Your current response rate is {performance['ctr']}.",
                "A small improvement can help turn more attention into customers."
            ))

        topic = (
            trigger_payload.get("keyword")
            or trigger_payload.get("topic")
            or trigger_payload.get("service")
            or trigger_payload.get("festival")
        )
        if topic:
            selected.append((
                f"Nearby demand around {topic} is rising.",
                "That makes this a strong moment to act."
            ))

        if evidence.get("customer_name"):
            selected.append((
                f"It is time for {evidence['customer_name']}'s next appointment.",
                "A timely reminder can improve attendance."
            ))

        if not selected and plan.get("summary"):
            selected.append((
                plan["summary"],
                "This is worth acting on now."
            ))

        items = []
        for fact, why in selected[:3]:
            items.append(f"{fact} {why}")

        return items

    def _enforce_limits(self, message: str) -> str:
        words = message.split()
        if len(words) > 100:
            return " ".join(words[:95]).rstrip() + "..."
        return message
