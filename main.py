Using **brainstorming** skill to design the errors module.

I've explored the codebase and found:

**Current state:**
- 10+ custom exceptions scattered across `imap/client.py`, `smtp/client.py`, `imap/oauth2_manager.py`
- MCP tools use plain `ValueError` for "not found" cases
- No unified base class, no MCP-specific error types
- No mapping layer from domain exceptions to MCP error responses

**Question:** Should this module:

A) **Consolidate only** — move existing inline exceptions to a central `errors/` package with a shared base class, keeping behavior unchanged

B) **Consolidate + MCP mapping** — do A, plus add MCP-specific exceptions and a mapping layer that converts domain errors to MCP-compatible error responses

C) **Full rewrite** — design a fresh exception hierarchy from scratch, replacing the existing IMAP/SMTP/OAuth2 exceptions entirely