from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from core.composer import Composer

app = FastAPI(title="Vera AI Bot")

composer = Composer()
conversation_memory = {}

# In-memory context store
context_db = {
    "category": {},
    "merchant": {},
    "customer": {},
    "trigger": {}
}


class ContextRequest(BaseModel):
    scope: str
    context_id: str
    version: int
    payload: Dict[str, Any]
    delivered_at: str


class TickRequest(BaseModel):
    now: str
    available_triggers: List[str]


class ReplyRequest(BaseModel):
    conversation_id: str
    merchant_id: str
    customer_id: Optional[str] = None
    from_role: str
    message: str
    received_at: str
    turn_number: int


@app.get("/v1/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/v1/metadata")
def metadata():
    return {
        "team_name": "DIMPI_BOT",
        "bot_name": "Vera AI Bot",
        "model": "Deterministic Composer",
        "version": "0.1"
    }


@app.post("/v1/context")
def push_context(req: ContextRequest):

    context_db.setdefault(req.scope, {})

    context_db[req.scope][req.context_id] = req.payload

    return {
        "accepted": True,
        "ack_id": f"ack_{req.context_id}",
        "stored_at": req.delivered_at
    }


@app.post("/v1/tick")
def tick(req: TickRequest):

    actions = []

    for trigger_id in req.available_triggers:

        trigger = context_db["trigger"].get(trigger_id)

        if trigger is None:
            continue

        merchant = context_db["merchant"].get(
            trigger["merchant_id"]
        )

        if merchant is None:
            continue

        customer = None

        customer_id = trigger.get("customer_id")

        if customer_id:
            customer = context_db["customer"].get(customer_id)

        category = context_db["category"].get(
            merchant["category_slug"]
        )

        context = {
            "category": category,
            "merchant": merchant,
            "customer": customer,
            "trigger": trigger
        }

        action = composer.compose(context)

        if action:

         conversation_id = (
         f"{action['merchant_id']}:"
         f"{action['trigger_id']}"
        )

         conversation_memory[conversation_id] = {
         "merchant_id": action["merchant_id"],
         "trigger_id": action["trigger_id"],
         "customer_id": action.get("customer_id"),
         "last_action": action,
         "state": "waiting"
       }
         print("Stored conversation:", conversation_id)
         action["conversation_id"] = conversation_id

         actions.append(action)

         return {
        "actions": actions
       }


@app.post("/v1/reply")
def reply(req: ReplyRequest):
    
    print("\n========== REPLY RECEIVED ==========")
    print("Conversation ID:", req.conversation_id)
    print("Merchant ID:", req.merchant_id)
    print("Customer ID:", req.customer_id)
    print("Message:", req.message)
    print("Memory Keys:", list(conversation_memory.keys()))
    print("===================================\n")

    memory = conversation_memory.get(req.conversation_id)

    if memory is None:
        for conv in conversation_memory.values():
            if conv.get("merchant_id") == req.merchant_id:
                memory = conv
                break

    if memory is None:
        memory = {
            "merchant_id": req.merchant_id,
            "trigger_id": None,
            "customer_id": req.customer_id,
            "last_action": {"merchant_id": req.merchant_id},
            "state": "waiting"
        }
        conversation_memory[req.conversation_id] = memory

    text = req.message.lower().strip()

    hostile = [
        "spam",
        "stop",
        "leave me",
        "don't message",
        "do not message",
        "useless",
        "annoying",
        "never"
    ]

    if any(word in text for word in hostile):

        memory["state"] = "closed"

        return {
            "action": "end"
        }

    auto = [
        "out of office",
        "automatic reply",
        "auto reply",
        "vacation",
        "i am away",
        "i'll get back",
        "currently unavailable"
    ]

    if any(word in text for word in auto):

        memory["state"] = "closed"

        return {
            "action": "end"
        }

    positive = [
        "yes",
        "ok",
        "okay",
        "sure",
        "let's do it",
        "lets do it",
        "sounds good",
        "go ahead",
        "what next",
        "what's next",
        "next",
        "continue",
        "proceed",
        "done"
    ]

    if any(word in text for word in positive):

        trigger = context_db["trigger"].get(
            memory.get("trigger_id")
        )

        kind = None

        if trigger is not None:
            kind = trigger.get("kind")

        follow_up = {

            "research_digest":
                "Great! I can proceed with the next step and prepare the campaign using today's research insights.",

            "perf_dip":
                "Perfect! I can proceed with the next step and walk you through the key recommendations that can improve your business performance.",

            "festival_upcoming":
                "Awesome! I can proceed with the next step and help create a festival campaign using your active offers.",

            "renewal_due":
                "Great! I can proceed with the next step by reviewing your renewal details and confirming the subscription.",

            "recall_due":
                "Perfect! I can proceed with the next step by preparing the appointment reminder so it can be sent to the customer.",

            "regulation_change":
                "Sure! I can proceed with the next step by highlighting the important regulatory changes that may affect your business."
        }

        memory["state"] = "completed"

        reply_text = follow_up.get(
            kind,
            "Great! I can proceed with the next step."
        )

        return {
            "action": "reply",
            "message": reply_text,
            "body": reply_text
        }

    return {
        "action": "end"
    }