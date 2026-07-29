from core.message_generator import MessageGenerator


def test_generates_plan_driven_message_with_clear_cta():
    generator = MessageGenerator()
    plan = {
        "owner_name": "Asha",
        "cta": "Review the recommendation",
        "summary": "Your recent performance deserves attention.",
        "evidence": {
            "trigger_kind": "perf_dip",
            "trigger_payload": {
                "keyword": "dentist"
            },
            "performance": {
                "views": 120,
                "ctr": 0.8
            },
            "has_active_offer": True,
            "offers": [{"price": 499}]
        }
    }

    message = generator.generate(plan)

    words = message.split()
    assert len(words) <= 100
    assert message.startswith("Hi Asha,")
    assert "Review the recommendation" in message or "review the recommendation" in message.lower()
    assert "benefit" not in message.lower() or "help" in message.lower()
    assert "views" not in message.lower() and "ctr" not in message.lower()
    assert "keyword" not in message.lower()
    assert "price" not in message.lower()
