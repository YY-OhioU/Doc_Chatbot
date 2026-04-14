import json

from app.interfaces.llm import LLMClient


class VerifierAgent:
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    def verify(self, query: str, draft_answer: str, evidence: list[dict]) -> dict:
        evidence_lines = [
            f"- {item.get('paper_id', 'unknown')}::{item.get('section_id', 'unknown')}: {item.get('text', '')}"
            for item in evidence[:8]
        ]
        system = "You are a strict verifier. Return JSON only."
        user = (
            "Check whether the answer is supported by evidence. Return JSON: "
            "{\"is_supported\": bool, \"confidence\": number, \"issues\": [str], \"revision_guidance\": str}.\n"
            f"Question: {query}\n\nDraft answer:\n{draft_answer}\n\n"
            f"Evidence:\n{chr(10).join(evidence_lines)}"
        )
        raw = self.llm.complete(system, user)
        try:
            parsed = json.loads(raw)
            parsed.setdefault("is_supported", False)
            parsed.setdefault("confidence", 0.0)
            parsed.setdefault("issues", [])
            parsed.setdefault("revision_guidance", "")
            return parsed
        except json.JSONDecodeError:
            return {
                "is_supported": False,
                "confidence": 0.2,
                "issues": ["Verifier returned non-JSON response."],
                "revision_guidance": "Retry with clearer evidence linkage.",
            }
