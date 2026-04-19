"""Configuration helpers for the MCP email service."""

from __future__ import annotations

import os
from dataclasses import dataclass

from errors import ConfigurationError


@dataclass(frozen=True)
class IMAPConfig:
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = True
    mailbox: str = "INBOX"

    def validate(self) -> None:
        if not self.host:
            raise ConfigurationError("IMAP host is required")
        if not self.username:
            raise ConfigurationError("IMAP username is required")
        if not self.password:
            raise ConfigurationError("IMAP password is required")
        if self.port <= 0:
            raise ConfigurationError("IMAP port must be greater than 0")



def load_imap_config_from_env() -> IMAPConfig:
    config = IMAPConfig(
        host=os.getenv("IMAP_HOST", ""),
        port=int(os.getenv("IMAP_PORT", "993")),
        username=os.getenv("IMAP_USERNAME", ""),
        password=os.getenv("IMAP_PASSWORD", ""),
        use_tls=os.getenv("IMAP_USE_TLS", "true").lower() != "false",
        mailbox=os.getenv("IMAP_MAILBOX", "INBOX"),
    )
    config.validate()
    return config
