# Multi-Agent + Tool PDF QA (MVP Scaffold)

Lightweight local CLI scaffold for experimenting with a multi-agent, tool-driven PDF question-answering pipeline.

## What this includes

- CLI entrypoint (`main_cli.py`)
- Looping orchestrator with verifier-driven retry capability
- Shared run state object
- Structured trace/event logging
- Agent modules:
  - Planner (LLM-driven)
  - Synthesizer (LLM-driven)
  - Verifier (LLM-driven)
- Tool modules:
  - Paper locator
  - Section locator
  - Passage reader
- LLM abstraction + OpenAI-compatible client for local vLLM

## Run

1) Install dependencies:

```bash
pip install openai
```

2) Ensure your local vLLM server is running in OpenAI-compatible mode (example: `http://127.0.0.1:8000/v1`).

3) Set environment variables (optional defaults shown):

```bash
export LLM_PROVIDER=openai_compat
export LLM_BASE_URL=http://127.0.0.1:8000/v1
export LLM_API_KEY=local-dev-key
export LLM_MODEL=Qwen/Qwen2.5-7B-Instruct
```

4) Run CLI:

```bash
python main_cli.py
```

### Mock mode (for local smoke tests without vLLM)

```bash
export LLM_PROVIDER=mock
python main_cli.py
```

## Pipeline stages

1. User question input
2. Planner
3. Paper locator
4. Section locator
5. Synthesizer
6. Verifier
7. Retry/replan loop if verifier rejects
8. Final answer output

## Notes

- This is an intentionally minimal scaffold, not a production QA system.
- Retrieval logic is placeholder/stubbed for future upgrades.
- Modules are structured to make it easy to add memory, retries, replanning, stronger retrieval, alternative LLM backends, and future service interfaces.
