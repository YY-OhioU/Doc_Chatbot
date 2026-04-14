from app.interfaces.llm import LLMClient


class MockLLM(LLMClient):
    def complete(self, system_prompt: str, user_prompt: str) -> str:
        short = f"SYS: {system_prompt} USER: {user_prompt}".strip().replace("\n", " ")
        return f"[MockLLM response] {short[:240]}"
