import os
from openai import OpenAI


class LLMService:
    """
    Handles all communication with the LLM.
    """

    def __init__(self):

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable not found."
            )

        self.client = OpenAI(api_key=api_key)

    def generate_message(self, prompt):

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": prompt["system"]
                },
                {
                    "role": "user",
                    "content": prompt["user"]
                }
            ],
            temperature=0.4,
            max_tokens=180
        )

        return response.choices[0].message.content.strip()