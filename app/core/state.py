from dataclasses import dataclass, field
from typing import Any


@dataclass
class RunState:
    user_query: str
    plan: list[str] = field(default_factory=list)
    candidate_papers: list[dict[str, Any]] = field(default_factory=list)
    candidate_sections: list[dict[str, Any]] = field(default_factory=list)
    collected_evidence: list[dict[str, Any]] = field(default_factory=list)
    draft_answer: str = ""
    verifier_result: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    final_answer: str = ""
    iteration: int = 0
    max_iterations: int = 0
    verifier_history: list[dict[str, Any]] = field(default_factory=list)
