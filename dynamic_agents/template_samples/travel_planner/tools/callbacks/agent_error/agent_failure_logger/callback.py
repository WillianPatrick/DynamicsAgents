"""Callback that records agent level failures in the runtime state."""

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
        agent_failures = state.setdefault("_agent_failures", [])
        agent_failures.append(
            {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "agent": payload.get("agent"),
                "reason": payload.get("reason"),
            }
        )
        state.setdefault("_events", []).append(
            {
                "name": "agent_failure_recorded",
                "payload": {
                    "agent": payload.get("agent"),
                    "reason": payload.get("reason"),
                },
            }
        )
        return {"agent_failures": agent_failures}
