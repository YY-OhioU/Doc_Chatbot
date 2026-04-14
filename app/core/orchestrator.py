from datetime import datetime, timezone

from app.agents.planner import PlannerAgent
from app.agents.synthesizer import SynthesizerAgent
from app.agents.verifier import VerifierAgent
from app.core.state import RunState
from app.infra.trace import TraceLogger
from app.tools.paper_locator import PaperLocator
from app.tools.passage_reader import PassageReader
from app.tools.section_locator import SectionLocator


class QAOrchestrator:
    def __init__(self, trace_logger: TraceLogger) -> None:
        self.trace = trace_logger
        self.planner = PlannerAgent()
        self.paper_locator = PaperLocator()
        self.section_locator = SectionLocator()
        self.reader = PassageReader()
        self.synthesizer = SynthesizerAgent()
        self.verifier = VerifierAgent()

    def run(self, user_query: str) -> RunState:
        state = RunState(user_query=user_query)
        state.metadata["started_at"] = datetime.now(timezone.utc).isoformat()

        self.trace.emit("planner_started", {"query": user_query})
        state.plan = self.planner.plan(user_query)
        self.trace.emit("planner_finished", {"plan": state.plan})

        self.trace.emit("tool_called", {"tool": "paper_locator"})
        state.candidate_papers = self.paper_locator.find_papers(state.plan)
        self.trace.emit("tool_result", {"tool": "paper_locator", "count": len(state.candidate_papers)})

        self.trace.emit("tool_called", {"tool": "section_locator"})
        state.candidate_sections = self.section_locator.find_sections(state.candidate_papers, state.plan)
        self.trace.emit("tool_result", {"tool": "section_locator", "count": len(state.candidate_sections)})

        self.trace.emit("tool_called", {"tool": "passage_reader"})
        state.collected_evidence = self.reader.read_passages(state.candidate_sections)
        self.trace.emit("tool_result", {"tool": "passage_reader", "count": len(state.collected_evidence)})

        state.draft_answer = self.synthesizer.synthesize(
            query=state.user_query,
            plan=state.plan,
            evidence=state.collected_evidence,
        )
        self.trace.emit("synthesis_finished", {"draft_length": len(state.draft_answer)})

        state.verifier_result = self.verifier.verify(
            query=state.user_query,
            draft_answer=state.draft_answer,
            evidence=state.collected_evidence,
        )
        self.trace.emit("verifier_finished", state.verifier_result)

        state.final_answer = state.draft_answer
        if not state.verifier_result.get("is_supported", False):
            state.final_answer += "\n\n[Verifier note] This draft may be weakly supported by evidence."

        state.metadata["finished_at"] = datetime.now(timezone.utc).isoformat()
        self.trace.emit("final_answer", {"answer_preview": state.final_answer[:200]})
        return state
