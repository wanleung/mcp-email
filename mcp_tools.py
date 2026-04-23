"""MCP tool call wrappers."""

from __future__ import annotations

from errors import handle_tool_errors
from imap_client import IMAPClient


class MCPTools:
    def __init__(self, client: IMAPClient) -> None:
        self._client = client

    @handle_tool_errors
    def fetch_email(self, uid: str, mailbox: str | None = None) -> dict:
        return {"ok": True, "data": self._client.fetch_email(uid=uid, mailbox=mailbox)}

    @handle_tool_errors
    def get_attachments(self, uid: str, filename: str | None = None, mailbox: str | None = None) -> dict:
        return {
            "ok": True,
            "data": self._client.get_attachments(uid=uid, filename=filename, mailbox=mailbox),
        }
