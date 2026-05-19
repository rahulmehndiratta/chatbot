from services.providers.ollama_provider import OllamaProvider

class AIService:
    def __init__(self, provider="ollama"):
        if provider == "ollama":
            self.provider = OllamaProvider()
        # future:
        # elif provider == "openai":
        #     self.provider = OpenAIProvider()

    def ask(self, prompt: str):
        return self.provider.generate(prompt)