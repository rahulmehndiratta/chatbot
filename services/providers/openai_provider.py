from openai import OpenAI

class OpenAIProvider:
    def __init__(self):
        self.client = OpenAI(api_key="your-key")

    def generate(self, prompt: str):
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content