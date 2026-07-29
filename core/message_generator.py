from typing import Dict, List


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

        facts = self._render_facts(plan.get("facts", []))

        for sentence in facts:
            lines.append(sentence)

        cta = plan.get("cta") or "Take action"
        cta_text = f"{cta}."
        lines.append(f"\n{cta_text}")

        message = " ".join(lines)
        return self._enforce_limits(message, cta_text)

    def _render_facts(self, facts: List[str]) -> List[str]:
        return [
            f"{fact} This makes it worth acting on now."
            for fact in facts[:3]
        ]

    def _enforce_limits(self, message: str, cta: str) -> str:
        words = message.split()
        if len(words) > 100:
            cta_words = len(cta.split())
            body_limit = max(1, 100 - cta_words - 1)
            body = " ".join(words[:body_limit]).rstrip(" .,;:")
            return f"{body}... {cta}"
        return message
