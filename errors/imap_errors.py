"""IMAP domain exceptions."""

from __future__ import annotations

from .base import MCPEmailServiceError


class ConfigurationError(MCPEmailServiceError):
    code = "configuration_error"


class IMAPConnectionError(MCPEmailServiceError):
    code = "imap_connection_error"


class IMAPAuthenticationError(MCPEmailServiceError):
    code = "imap_authentication_error"


class EmailNotFoundError(MCPEmailServiceError):
    code = "email_not_found"


class AttachmentNotFoundError(MCPEmailServiceError):
    code = "attachment_not_found"
