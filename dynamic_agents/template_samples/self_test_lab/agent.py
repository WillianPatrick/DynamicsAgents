"""Exports the Self-Test Lab app built from the workflow definition."""

from __future__ import annotations

import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from dynamic_agents import DynamicAgentRuntime

_RUNTIME = DynamicAgentRuntime(APP_ROOT)
app = _RUNTIME.build_adk_app("self_test_lab")
root_agent = app.root_agent

__all__ = ["app", "root_agent"]
