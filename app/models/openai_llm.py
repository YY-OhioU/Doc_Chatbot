import os

from openai import OpenAI

from app.interfaces.llm import LLMClient


class OpenAICompatLLM(LLMClient):
    """OpenAI-compatible client for local vLLM endpoints."""

    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout_seconds: float = 60.0,
    ) -> None:
        self.model = model or os.getenv("LLM_MODEL", "Qwen/Qwen2.5-7B-Instruct")
        self.client = OpenAI(
            base_url=base_url or os.getenv("LLM_BASE_URL", "http://127.0.0.1:8000/v1"),
            api_key=api_key or os.getenv("LLM_API_KEY", "local-dev-key"),
            timeout=timeout_seconds,
        )

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content or ""
