# Multi-Agent + Tool PDF QA (MVP Scaffold)

Lightweight local CLI scaffold for experimenting with a multi-agent, tool-driven PDF question-answering pipeline.

## What this includes

- CLI entrypoint (`main_cli.py`)
- Orchestrator with full pipeline stages
- Shared run state object
- Structured trace/event logging
- Agent modules:
  - Planner
  - Synthesizer
  - Verifier
- Tool modules:
  - Paper locator
  - Section locator
  - Passage reader
- LLM abstraction + mock implementation

## Run

```bash
python main_cli.py
```

Then type a question and the CLI will print intermediate pipeline events and a final answer.

## Pipeline stages

1. User question input
2. Planner
3. Paper locator
4. Section locator
5. Synthesizer
6. Verifier
7. Final answer output

## Notes

- This is an intentionally minimal scaffold, not a production QA system.
- Retrieval logic is placeholder/stubbed for future upgrades.
- Modules are structured to make it easy to add memory, retries, replanning, stronger retrieval, alternative LLM backends, and future service interfaces.
