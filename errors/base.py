"""Base exception types for MCP Email service."""

from __future__ import annotations


class MCPEmailServiceError(Exception):
    """Base domain exception for the service."""

    code = "internal_error"

    def __init__(self, message: str, *, details: dict | None = None) -> None:
        super().__init__(message)
        self.details = details or {}
