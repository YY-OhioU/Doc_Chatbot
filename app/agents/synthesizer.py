from app.models.mock_llm import MockLLM


class SynthesizerAgent:
    def __init__(self) -> None:
        self.llm = MockLLM()

    def synthesize(self, query: str, plan: list[str], evidence: list[dict]) -> str:
        evidence_lines = [
            f"- {item.get('paper_id', 'unknown')}::{item.get('section_id', 'unknown')}: {item.get('text', '')}"
            for item in evidence[:3]
        ]
        prompt = (
            f"Question: {query}\n"
            f"Plan: {plan}\n"
            f"Evidence:\n" + "\n".join(evidence_lines)
        )
        return self.llm.complete(prompt)
