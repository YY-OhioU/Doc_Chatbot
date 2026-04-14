from app.core.orchestrator import QAOrchestrator
from app.infra.trace import TraceLogger


def main() -> None:
    print("=== Multi-Agent PDF QA MVP (CLI) ===")
    query = input("Ask a question: ").strip()
    if not query:
        print("No question entered. Exiting.")
        return

    trace = TraceLogger()
    orchestrator = QAOrchestrator(trace_logger=trace)
    state = orchestrator.run(query)

    print("\n--- Final Answer ---")
    print(state.final_answer or "No answer generated.")


if __name__ == "__main__":
    main()
