"""Stateless IMAP client wrapper."""

from __future__ import annotations

import base64
import imaplib
from contextlib import contextmanager
from email import message_from_bytes
from email.message import Message

from config import IMAPConfig
from email_parser import extract_text_and_html
from errors import (
    AttachmentNotFoundError,
    EmailNotFoundError,
    IMAPAuthenticationError,
    IMAPConnectionError,
)


class IMAPClient:
    def __init__(self, config: IMAPConfig) -> None:
        self._config = config

    @contextmanager
    def _connect(self):
        client = None
        try:
            client = (
                imaplib.IMAP4_SSL(self._config.host, self._config.port)
                if self._config.use_tls
                else imaplib.IMAP4(self._config.host, self._config.port)
            )
            client.login(self._config.username, self._config.password)
            yield client
        except imaplib.IMAP4.error as exc:
            message = str(exc).lower()
            if "auth" in message or "login" in message:
                raise IMAPAuthenticationError("IMAP authentication failed") from exc
            raise IMAPConnectionError("Failed to connect to IMAP server") from exc
        except OSError as exc:
            raise IMAPConnectionError("Failed to connect to IMAP server") from exc
        finally:
            try:
                if client is not None:
                    client.logout()
            except Exception:
                pass

    def _fetch_message(self, uid: str, mailbox: str | None = None) -> Message:
        selected_mailbox = mailbox or self._config.mailbox
        with self._connect() as client:
            status, _ = client.select(selected_mailbox)
            if status != "OK":
                raise IMAPConnectionError(f"Unable to select mailbox '{selected_mailbox}'")

            status, data = client.uid("fetch", uid, "(RFC822)")
            if status != "OK" or not data or data[0] is None:
                raise EmailNotFoundError(f"Email with UID {uid} not found")

            raw_email = data[0][1]
            if not isinstance(raw_email, (bytes, bytearray)):
                raise EmailNotFoundError(f"Email with UID {uid} not found")
            return message_from_bytes(raw_email)

    def fetch_email(self, uid: str, mailbox: str | None = None) -> dict:
        message = self._fetch_message(uid, mailbox)
        text_body, html_body = extract_text_and_html(message)
        return {
            "uid": uid,
            "from": message.get("From", ""),
            "to": message.get("To", ""),
            "subject": message.get("Subject", ""),
            "date": message.get("Date", ""),
            "text_body": text_body,
            "html_body": html_body,
        }

    def get_attachments(self, uid: str, filename: str | None = None, mailbox: str | None = None) -> list[dict]:
        message = self._fetch_message(uid, mailbox)
        attachments = []
        for part in message.walk():
            if part.get_content_disposition() != "attachment":
                continue
            part_filename = part.get_filename() or "attachment"
            if filename and part_filename != filename:
                continue
            payload = part.get_payload(decode=True)
            if payload is None:
                payload = b""
            attachments.append(
                {
                    "filename": part_filename,
                    "content_type": part.get_content_type(),
                    "size": len(payload),
                    "content_base64": base64.b64encode(payload).decode("ascii"),
                }
            )

        if filename and not attachments:
            raise AttachmentNotFoundError(f"Attachment '{filename}' not found for UID {uid}")
        return attachments
