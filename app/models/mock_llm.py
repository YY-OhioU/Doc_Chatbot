from app.interfaces.llm import LLMClient


class MockLLM(LLMClient):
    def complete(self, prompt: str) -> str:
        short = prompt.strip().replace("\n", " ")
        return f"[MockLLM response] {short[:180]}"
