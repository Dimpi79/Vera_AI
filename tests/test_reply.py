import unittest

from app import ReplyRequest, context_db, conversation_memory, reply


class ReplyFlowTests(unittest.TestCase):
    def test_commitment_reply_is_action_oriented(self):
        conversation_memory.clear()
        context_db["trigger"].clear()

        conversation_memory["conv_test"] = {
            "merchant_id": "m_test",
            "trigger_id": "t_test",
            "state": "waiting"
        }
        context_db["trigger"]["t_test"] = {"kind": "perf_dip"}

        req = ReplyRequest(
            conversation_id="conv_test",
            merchant_id="m_test",
            customer_id=None,
            from_role="merchant",
            message="Ok lets do it. What's next?",
            received_at="2026-07-29T00:00:00Z",
            turn_number=1,
        )

        response = reply(req)

        self.assertEqual(response["action"], "reply")
        self.assertEqual(response["body"], response["message"])
        body = response["message"].lower()
        self.assertTrue(any(word in body for word in ["proceed", "next", "draft", "confirm", "sending", "done"]))
        self.assertNotIn("would you", body)
        self.assertNotIn("do you", body)
        self.assertNotIn("can you", body)

    def test_commitment_reply_without_existing_memory(self):
        conversation_memory.clear()
        context_db["trigger"].clear()

        req = ReplyRequest(
            conversation_id="conv_intent_1",
            merchant_id="m_test",
            customer_id=None,
            from_role="merchant",
            message="Ok lets do it. What's next?",
            received_at="2026-07-29T00:00:00Z",
            turn_number=2,
        )

        response = reply(req)

        self.assertEqual(response["action"], "reply")
        self.assertEqual(response["body"], response["message"])
        self.assertIn("conv_intent_1", conversation_memory)
        self.assertEqual(conversation_memory["conv_intent_1"]["state"], "completed")


if __name__ == "__main__":
    unittest.main()
