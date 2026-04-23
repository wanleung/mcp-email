"""MCP server construction."""

from __future__ import annotations

from config import load_imap_config_from_env
from imap_client import IMAPClient
from mcp_tools import MCPTools


class MCPEmailServer:
    def __init__(self) -> None:
        config = load_imap_config_from_env()
        self.tools = MCPTools(IMAPClient(config))

    def health(self) -> dict:
        return {"status": "healthy", "service": "mcp-email"}



def create_server() -> MCPEmailServer:
    return MCPEmailServer()
