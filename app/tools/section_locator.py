
class SectionLocator:
    def find_sections(self, papers: list[dict], plan: list[str]) -> list[dict]:
        sections: list[dict] = []
        for p in papers:
            sections.append(
                {
                    "paper_id": p["paper_id"],
                    "section_id": "intro",
                    "section_title": "Introduction",
                }
            )
        return sections
