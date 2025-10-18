"""Callback that keeps a telemetry log for tool executions during the session."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional


class Callback:
    """Collects execution metadata for observability and playback."""

    def __init__(self, metadata: Optional[Dict[str, Any]] = None):
        self.metadata = metadata or {}

    def handle_event(
        self,
        event: str,
        payload: Dict[str, Any],
        state: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        state = state or {}
        testing_state = state.setdefault("testing", {})
        events = testing_state.setdefault("events", [])
        entry = {
            "event": event,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tool": payload.get("tool"),
            "method": payload.get("method"),
            "status": payload.get("status"),
            "agent": payload.get("agent"),
            "alias": payload.get("alias"),
        }
        if payload.get("error"):
            entry["error"] = str(payload["error"])
        events.append(entry)
        testing_state["events"] = events
        return {"testing": {"events": events}}
