from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class TraceEvent:
    timestamp: str
    name: str
    payload: dict[str, Any]


class TraceLogger:
    def __init__(self) -> None:
        self.events: list[TraceEvent] = []

    def emit(self, name: str, payload: dict[str, Any]) -> None:
        event = TraceEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            name=name,
            payload=payload,
        )
        self.events.append(event)
        print(f"[{event.name}] {event.payload}")
