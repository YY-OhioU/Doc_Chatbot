
class VerifierAgent:
    def verify(self, query: str, draft_answer: str, evidence: list[dict]) -> dict:
        supported = len(evidence) > 0 and len(draft_answer.strip()) > 0
        return {
            "query": query,
            "is_supported": supported,
            "evidence_count": len(evidence),
            "notes": "Placeholder verifier. Replace with stricter checks later.",
        }
