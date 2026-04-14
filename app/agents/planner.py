import json

from app.interfaces.llm import LLMClient


class PlannerAgent:
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    def plan(self, query: str, feedback: str = "") -> list[str]:
        system = "You are a planning agent for document QA. Return JSON only."
        user = (
            "Create up to 4 concise subquestions to answer the query using document evidence. "
            "Respond as JSON with key 'subquestions' as a list of strings.\n"
            f"Query: {query}\n"
            f"Verifier feedback (if any): {feedback}"
        )
        raw = self.llm.complete(system, user)
        try:
            parsed = json.loads(raw)
            subquestions = parsed.get("subquestions", [])
            if isinstance(subquestions, list) and subquestions:
                return [str(x) for x in subquestions][:4]
        except json.JSONDecodeError:
            pass
        return [
            f"Identify likely papers related to: {query}",
            "Locate sections that directly answer the question",
            "Synthesize evidence into a concise response",
        ]
