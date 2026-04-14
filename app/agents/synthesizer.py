from app.interfaces.llm import LLMClient


class SynthesizerAgent:
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    def synthesize(self, query: str, plan: list[str], evidence: list[dict]) -> str:
        evidence_lines = [
            f"- {item.get('paper_id', 'unknown')}::{item.get('section_id', 'unknown')}: {item.get('text', '')}"
            for item in evidence[:8]
        ]
        system = "You are a synthesis agent. Produce a direct answer grounded in provided evidence."
        user = (
            f"Question: {query}\n\n"
            f"Plan:\n- " + "\n- ".join(plan) + "\n\n"
            "Evidence:\n" + "\n".join(evidence_lines) + "\n\n"
            "Write a concise answer followed by bullet points for cited evidence snippets."
        )
        return self.llm.complete(system, user)
