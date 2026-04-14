import os

from app.interfaces.llm import LLMClient
from app.models.mock_llm import MockLLM


def build_llm_client() -> LLMClient:
    provider = os.getenv("LLM_PROVIDER", "openai_compat").lower()
    if provider == "mock":
        return MockLLM()

    from app.models.openai_llm import OpenAICompatLLM

    return OpenAICompatLLM()
