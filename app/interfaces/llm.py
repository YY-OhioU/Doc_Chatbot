from typing import Protocol


class LLMClient(Protocol):
    def complete(self, system_prompt: str, user_prompt: str) -> str:
        ...
