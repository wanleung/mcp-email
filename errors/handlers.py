"""Decorator utilities for converting exceptions to MCP errors."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any

from .mcp_mapping import to_mcp_error


def handle_tool_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001 - centralized mapper
            return to_mcp_error(exc)

    return wrapper
