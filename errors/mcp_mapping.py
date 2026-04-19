"""Maps service exceptions to structured MCP-compatible payloads."""

from __future__ import annotations

from .base import MCPEmailServiceError


def to_mcp_error(exc: Exception) -> dict:
    if isinstance(exc, MCPEmailServiceError):
        return {
            "ok": False,
            "error": {
                "code": exc.code,
                "message": str(exc),
                "details": exc.details,
            },
        }

    return {
        "ok": False,
        "error": {
            "code": "internal_error",
            "message": "An unexpected error occurred",
            "details": {},
        },
    }
