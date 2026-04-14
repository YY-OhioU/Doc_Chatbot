from app.core.orchestrator import QAOrchestrator
from app.infra.trace import TraceLogger
from app.models.factory import build_llm_client


def main() -> None:
    print("=== Multi-Agent PDF QA MVP (CLI) ===")
    query = input("Ask a question: ").strip()
    if not query:
        print("No question entered. Exiting.")
        return

    trace = TraceLogger()
    llm = build_llm_client()
    orchestrator = QAOrchestrator(trace_logger=trace, llm=llm, max_iterations=3)
    state = orchestrator.run(query)

    print("\n--- Final Answer ---")
    print(state.final_answer or "No answer generated.")
    print(f"\n(Completed in {state.iteration}/{state.max_iterations} iteration(s))")


if __name__ == "__main__":
    main()
