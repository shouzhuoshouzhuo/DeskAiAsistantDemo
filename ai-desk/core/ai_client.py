from openai import OpenAI
from config.settings import API_KEY, MODEL, BASE_URL


class AIClient:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    def chat(self, messages: list[dict]) -> str:
        response = self.client.chat.completions.create(
            model=MODEL,
            max_tokens=2048,
            messages=messages,
        )
        if isinstance(response, str):
            return response
        return response.choices[0].message.content