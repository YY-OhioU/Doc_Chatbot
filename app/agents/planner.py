
class PlannerAgent:
    def plan(self, query: str) -> list[str]:
        return [
            f"Identify likely papers related to: {query}",
            "Locate sections that directly answer the question",
            "Synthesize evidence into a concise response",
        ]
