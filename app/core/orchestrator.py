from datetime import datetime, timezone

from app.agents.planner import PlannerAgent
from app.agents.synthesizer import SynthesizerAgent
from app.agents.verifier import VerifierAgent
from app.core.state import RunState
from app.infra.trace import TraceLogger
from app.interfaces.llm import LLMClient
from app.tools.paper_locator import PaperLocator
from app.tools.passage_reader import PassageReader
from app.tools.section_locator import SectionLocator


class QAOrchestrator:
    def __init__(self, trace_logger: TraceLogger, llm: LLMClient, max_iterations: int = 3) -> None:
        self.trace = trace_logger
        self.planner = PlannerAgent(llm)
        self.paper_locator = PaperLocator()
        self.section_locator = SectionLocator()
        self.reader = PassageReader()
        self.synthesizer = SynthesizerAgent(llm)
        self.verifier = VerifierAgent(llm)
        self.max_iterations = max_iterations

    def run(self, user_query: str) -> RunState:
        state = RunState(user_query=user_query, max_iterations=self.max_iterations)
        state.metadata["started_at"] = datetime.now(timezone.utc).isoformat()

        feedback = ""
        for i in range(1, self.max_iterations + 1):
            state.iteration = i
            self.trace.emit("iteration_started", {"iteration": i})

            self.trace.emit("planner_started", {"query": user_query, "feedback": feedback})
            state.plan = self.planner.plan(user_query, feedback=feedback)
            self.trace.emit("planner_finished", {"iteration": i, "plan": state.plan})

            self.trace.emit("tool_called", {"tool": "paper_locator", "iteration": i})
            state.candidate_papers = self.paper_locator.find_papers(state.plan)
            self.trace.emit("tool_result", {"tool": "paper_locator", "count": len(state.candidate_papers)})

            self.trace.emit("tool_called", {"tool": "section_locator", "iteration": i})
            state.candidate_sections = self.section_locator.find_sections(state.candidate_papers, state.plan)
            self.trace.emit("tool_result", {"tool": "section_locator", "count": len(state.candidate_sections)})

            self.trace.emit("tool_called", {"tool": "passage_reader", "iteration": i})
            state.collected_evidence = self.reader.read_passages(state.candidate_sections)
            self.trace.emit("tool_result", {"tool": "passage_reader", "count": len(state.collected_evidence)})

            state.draft_answer = self.synthesizer.synthesize(
                query=state.user_query,
                plan=state.plan,
                evidence=state.collected_evidence,
            )
            self.trace.emit("synthesis_finished", {"iteration": i, "draft_length": len(state.draft_answer)})

            state.verifier_result = self.verifier.verify(
                query=state.user_query,
                draft_answer=state.draft_answer,
                evidence=state.collected_evidence,
            )
            state.verifier_history.append(state.verifier_result)
            self.trace.emit("verifier_finished", {"iteration": i, **state.verifier_result})

            if state.verifier_result.get("is_supported", False):
                state.final_answer = state.draft_answer
                self.trace.emit("iteration_finished", {"iteration": i, "status": "accepted"})
                break

            feedback = state.verifier_result.get("revision_guidance", "Improve evidence alignment.")
            self.trace.emit("iteration_finished", {"iteration": i, "status": "retrying", "feedback": feedback})

        if not state.final_answer:
            state.final_answer = state.draft_answer + "\n\n[Verifier note] Final draft may be weakly supported."

        state.metadata["finished_at"] = datetime.now(timezone.utc).isoformat()
        self.trace.emit("final_answer", {"answer_preview": state.final_answer[:200], "iterations": state.iteration})
        return state
