class PromptBuilder:
    """
    Builds the final prompt that will be sent to the LLM.
    """

    SYSTEM_PROMPT = """
You are Vera, an AI assistant for local businesses.

Your job is to write a natural WhatsApp message.

Rules:
1. Use ONLY the provided facts.
2. Never invent information.
3. Never invent discounts or offers.
4. Follow the provided message flow.
5. Keep the tone natural and conversational.
6. Keep the reply under 120 words.
7. Do not use markdown.
8. End with the provided call to action.
9. If the merchant has already committed or said "let's do it", switch to action mode and describe the next step clearly.
10. Do not ask a new qualifying question after commitment.
"""

    def build(self, plan):

        facts = "\n".join(
            f"- {fact}" for fact in plan["facts"]
        )

        personalization = "\n".join(
            f"- {item}" for item in plan["personalization"]
        )

        flow = "\n".join(
            f"- {step}" for step in plan["message_flow"]
        )

        avoid = "\n".join(
            f"- {item}" for item in plan["avoid"]
        )

        user_prompt = f"""
Recipient:
{plan['recipient']}

Intent:
{plan['intent']}

Goal:
{plan['goal']}

Tone:
{plan['tone']}

Opening:
{plan['opening']}

Personalization:
{personalization}

Message Flow:
{flow}

Facts:
{facts}

Call To Action:
{plan['cta']}

Restrictions:
{avoid}
"""

        return {
            "system": self.SYSTEM_PROMPT.strip(),
            "user": user_prompt.strip()
        }