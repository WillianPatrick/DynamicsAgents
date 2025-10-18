"""Callback that records tool execution failures into the runtime state."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional


class Callback:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata

    def handle_event(
        self,
        event: str,
        payload: Dict[str, Any],
        state: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if state is None:
            state = {}
        errors = state.setdefault("_errors", [])
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tool": payload.get("tool"),
            "method": payload.get("method"),
            "error": payload.get("error"),
        }
        errors.append(entry)
        state.setdefault("_events", []).append(
            {
                "name": "failure_logged",
                "payload": {
                    "tool": entry["tool"],
                    "method": entry["method"],
                    "error": entry["error"],
                },
            }
        )
        return {"errors": errors}
