
class PassageReader:
    def read_passages(self, sections: list[dict]) -> list[dict]:
        evidence = []
        for s in sections:
            evidence.append(
                {
                    "paper_id": s["paper_id"],
                    "section_id": s["section_id"],
                    "text": "Placeholder extracted passage text.",
                }
            )
        return evidence
