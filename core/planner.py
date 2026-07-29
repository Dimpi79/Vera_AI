from typing import Dict, List, Tuple


class Planner:
    """
    Converts the business decision into a communication plan.

    This class DOES NOT generate English sentences.

    It decides:
        • what information should be conveyed
        • what tone to use
        • which CTA to use
        • which facts are important
    """

    def build_plan(
        self,
        context: Dict,
        decision: Dict,
        evidence: Dict
    ):

        merchant = context.get("merchant", {})
        customer = context.get("customer") or {}
        trigger = context.get("trigger", {})

        plan = {

            "recipient": decision["audience"],

            "intent": decision["intent"],

            "goal": decision["goal"],

            "strategy": decision.get(
                "strategy",
                "inform"
            ),

            "priority": decision["priority"],

            "tone": self._tone(
                decision,
                evidence
            ),

            "opening": self._opening(
                evidence,
                customer
            ),

            "summary": self._summary(
                trigger,
                decision
            ),

            "facts": self._facts(
                trigger,
                evidence,
                decision
            ),

            "cta": self._cta(
                trigger,
                decision
            ),

            "reason_codes": decision.get(
                "reason",
                []
            ),

            "merchant_name": evidence.get(
                "merchant_name"
            ),

            "owner_name": evidence.get(
                "owner_name"
            ),

            "customer_name": evidence.get(
                "customer_name"
            ),

            "category": evidence.get(
                "category_slug"
            ),

            "evidence": evidence,

            "avoid": [
                "Never invent facts.",
                "Never invent offers.",
                "Never promise unavailable discounts.",
                "Keep message under 120 words."
            ]
        }

        return plan

    # --------------------------------------------------

    def _tone(self, decision, evidence):

        strategy = decision.get("strategy")

        if strategy == "coach":
            return "supportive"

        if strategy == "educate":
            return "helpful"

        if strategy == "retain":
            return "professional"

        if strategy == "promote":
            return "enthusiastic"

        if decision["priority"] == "critical":
            return "urgent"

        return "friendly"

    # --------------------------------------------------

    def _opening(
        self,
        evidence,
        customer
    ):

        if evidence.get("customer_name"):
            return f"Hi {evidence['customer_name']},"

        if evidence.get("owner_name"):
            return f"Hi {evidence['owner_name']},"

        identity = customer.get(
            "identity",
            {}
        )

        return f"Hi {identity.get('name','there')},"

    # --------------------------------------------------

    def _summary(
        self,
        trigger,
        decision
    ):

        summaries = {

            "research_digest":
                "We found something useful for your business.",

            "perf_dip":
                "Your recent performance deserves attention.",

            "festival_upcoming":
                "A seasonal opportunity is coming.",

            "renewal_due":
                "Your subscription needs attention.",

            "recall_due":
                "It's time for your next appointment.",

            "regulation_change":
                "There is an important regulatory update."
        }

        return summaries.get(
            trigger.get("kind"),
            decision["goal"]
        )

    # --------------------------------------------------

    def _facts(
        self,
        trigger,
        evidence,
        decision
    ):

        scored_facts: List[Tuple[float, str]] = []
        payload = trigger.get(
            "payload",
            {}
        )

        for key, value in payload.items():
            if isinstance(value, list):
                for item in value:
                    scored_facts.append(
                        self._score_fact(
                            str(item),
                            key,
                            evidence,
                            payload,
                            decision
                        )
                    )
            else:
                scored_facts.append(
                    self._score_fact(
                        f"{key.replace('_',' ').title()}: {value}",
                        key,
                        evidence,
                        payload,
                        decision
                    )
                )

        performance = evidence.get("performance") or {}
        if performance.get("views"):
            scored_facts.append(
                self._score_fact(
                    f"Your listing recently attracted {performance['views']} visits.",
                    "performance",
                    evidence,
                    payload,
                    decision
                )
            )

        if performance.get("ctr") is not None:
            scored_facts.append(
                self._score_fact(
                    f"Your current response rate is {performance['ctr']}.",
                    "performance",
                    evidence,
                    payload,
                    decision
                )
            )

        if evidence.get("has_active_offer"):
            scored_facts.append(
                self._score_fact(
                    "Merchant currently has active offers.",
                    "offer",
                    evidence,
                    payload,
                    decision
                )
            )

        if evidence.get("merchant_engaged"):
            scored_facts.append(
                self._score_fact(
                    "Merchant recently interacted with Vera.",
                    "engagement",
                    evidence,
                    payload,
                    decision
                )
            )

        scored_facts = self._deduplicate(scored_facts)
        scored_facts.sort(key=lambda item: item[0], reverse=True)

        selected = []
        used_categories = set()
        for score, fact in scored_facts:
            category = self._category_for_fact(fact)
            if category in used_categories:
                continue
            selected.append(fact)
            used_categories.add(category)
            if len(selected) >= 3:
                break

        if not selected:
            selected = [fact for _, fact in scored_facts[:1]]

        return selected

    def _score_fact(
        self,
        fact: str,
        key: str,
        evidence: Dict,
        payload: Dict,
        decision: Dict
    ) -> Tuple[float, str]:

        text = fact.lower()
        score = 0.0

        if "offer" in text or "discount" in text or "price" in text:
            score += 3.5
        if "visit" in text or "response" in text or "performance" in text:
            score += 4.0
        if "urgent" in text or "due" in text or "soon" in text or "upcoming" in text:
            score += 2.5
        if "topic" in text or "keyword" in text or "service" in text:
            score += 1.5
        if "engaged" in text or "interacted" in text:
            score += 0.8
        if evidence.get("has_active_offer") and "offer" in text:
            score += 1.0

        priority = decision.get("priority", "medium")
        if priority == "critical":
            score += 1.5
        elif priority == "high":
            score += 1.0

        if score <= 0:
            score = 0.5

        if payload.get(key) is not None and isinstance(payload.get(key), list):
            score += 0.2

        return score, fact

    def _category_for_fact(self, fact: str) -> str:
        text = fact.lower()
        if "offer" in text or "discount" in text or "price" in text:
            return "offer"
        if "visit" in text or "response" in text or "performance" in text:
            return "performance"
        if "urgent" in text or "due" in text or "soon" in text or "upcoming" in text:
            return "urgency"
        if "engaged" in text or "interacted" in text:
            return "engagement"
        return "other"

    def _deduplicate(
        self,
        facts: List[Tuple[float, str]]
    ) -> List[Tuple[float, str]]:

        seen = set()
        unique = []

        for item in facts:
            score, fact = item
            normalized = fact.strip().lower()
            if normalized in seen:
                continue
            seen.add(normalized)
            unique.append((score, fact))

        return unique

    # --------------------------------------------------

    def _cta(
        self,
        trigger,
        decision
    ):

        mapping = {

            "research_digest":
                "Read today's insight",

            "perf_dip":
                "Review the recommendation",

            "festival_upcoming":
                "Create a campaign",

            "renewal_due":
                "Renew now",

            "recall_due":
                "Book your appointment",

            "regulation_change":
                "Review the update"
        }

        return mapping.get(
            trigger.get("kind"),
            "Take action"
        )