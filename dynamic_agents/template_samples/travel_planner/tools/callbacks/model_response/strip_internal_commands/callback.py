"""Removes internal orchestration commands from model responses."""

from __future__ import annotations

from typing import Any, Dict, Iterable, Optional, Tuple

_COMMAND_PREFIXES: Tuple[str, ...] = ("@delegate", "@tool")


class Callback:
    """Strip `@delegate` and `@tool` lines from user-facing messages."""

    def __init__(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.metadata = metadata or {}

    def handle_event(
        self,
        event: str,
        payload: Dict[str, Any],
        state: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if event not in {"after_model_response", "model_response"}:
            return {}

        cleaned_payload, modified = _strip_payload(payload)
        if not modified:
            return {}

        if isinstance(state, dict):
            state.setdefault("_events", []).append(
                {"name": "commands_sanitized", "payload": {"stripped": True}}
            )
        return {"payload": cleaned_payload}


def _strip_payload(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    modified = False
    updated = dict(payload)

    for key in ("response", "text", "content", "parts"):
        if key not in payload:
            continue
        new_value, changed = _strip_structure(payload[key])
        if changed:
            updated[key] = new_value
            modified = True

    return (updated if modified else payload, modified)


def _strip_structure(value: Any) -> Tuple[Any, bool]:
    if isinstance(value, str):
        return _strip_text(value)
    if isinstance(value, list):
        items = []
        changed = False
        for item in value:
            new_item, item_changed = _strip_structure(item)
            if item_changed:
                changed = True
            items.append(new_item)
        return (items if changed else value, changed)
    if isinstance(value, dict):
        updated: Dict[str, Any] = {}
        changed = False
        for key, item in value.items():
            new_item, item_changed = _strip_structure(item)
            if item_changed:
                changed = True
            updated[key] = new_item
        return (updated if changed else value, changed)
    return value, False


def _strip_text(text: str) -> Tuple[str, bool]:
    lines = []
    changed = False
    for line in text.splitlines():
        if _is_command_line(line):
            changed = True
            continue
        lines.append(line)
    if not changed:
        return text, False
    return "\n".join(_trim_trailing_blank_lines(lines)), True


def _is_command_line(line: str) -> bool:
    stripped = line.lstrip()
    return any(stripped.startswith(prefix) for prefix in _COMMAND_PREFIXES)


def _trim_trailing_blank_lines(lines: Iterable[str]) -> Iterable[str]:
    trimmed = list(lines)
    while trimmed and not trimmed[-1].strip():
        trimmed.pop()
    return trimmed


__all__ = ["Callback"]
