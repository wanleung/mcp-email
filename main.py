"""Executable entrypoint for MCP Email Service (IMAP)."""

from __future__ import annotations

from errors import to_mcp_error
from mcp_server import create_server



def main() -> int:
    try:
        server = create_server()
        health = server.health()
        print(f"MCP Email Service ready: {health['status']}")
        return 0
    except Exception as exc:  # noqa: BLE001 - startup should never leak raw exception details
        error = to_mcp_error(exc)
        print(error["error"]["message"])
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
