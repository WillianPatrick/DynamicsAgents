"""Callback that builds a streaming transcript of model responses."""

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
        transcript = state.setdefault("transcript", [])
        agent_label = payload.get("agent_label") or payload.get("agent")
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event": event,
            "payload": payload,
        }
        if agent_label:
            entry["agent_label"] = agent_label
            display = None
            for key in ("message", "response", "content", "text"):
                value = payload.get(key)
                if isinstance(value, str):
                    stripped = value.strip()
                    if stripped:
                        display = stripped
                        break
            if display:
                entry["display"] = f"{agent_label}: {display}"
        transcript.append(entry)
        state.setdefault("_events", []).append(
            {
                "name": "stream_updated",
                "payload": {
                    "total_messages": len(transcript),
                },
            }
        )
        return {"transcript": transcript}
