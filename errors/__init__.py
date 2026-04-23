"""Error package exports."""

from .base import MCPEmailServiceError
from .handlers import handle_tool_errors
from .imap_errors import (
    AttachmentNotFoundError,
    ConfigurationError,
    EmailNotFoundError,
    IMAPAuthenticationError,
    IMAPConnectionError,
)
from .mcp_mapping import to_mcp_error

__all__ = [
    "AttachmentNotFoundError",
    "ConfigurationError",
    "EmailNotFoundError",
    "IMAPAuthenticationError",
    "IMAPConnectionError",
    "MCPEmailServiceError",
    "handle_tool_errors",
    "to_mcp_error",
]
