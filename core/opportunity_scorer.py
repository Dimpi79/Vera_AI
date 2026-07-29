from typing import Dict


class OpportunityScorer:
    """
    Scores how important an opportunity is.

    The output is later used to decide whether
    Vera should proactively message the merchant/customer.
    """

    PRIORITY_SCORE = {
        "low": 25,
        "medium": 50,
        "high": 75,
        "critical": 100
    }

    STATE_BONUS = {
        "active": 0,
        "lapsed_soft": 10,
        "lapsed_hard": 20
    }

    def score(self, evidence: Dict):

        score = self.PRIORITY_SCORE.get(
            evidence["priority"],
            50
        )

        state = evidence.get("customer_state")

        if state:
            score += self.STATE_BONUS.get(state, 0)

        score = min(score, 100)

        if score >= 80:
            level = "excellent"

        elif score >= 60:
            level = "good"

        elif score >= 40:
            level = "moderate"

        else:
            level = "low"

        return {
            "score": score,
            "level": level
        }