"""Email parsing helpers."""

from __future__ import annotations

from email.message import Message


def extract_text_and_html(message: Message) -> tuple[str | None, str | None]:
    text_body: str | None = None
    html_body: str | None = None

    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            if part.get_content_disposition() == "attachment":
                continue
            payload = part.get_payload(decode=True)
            if not payload:
                continue
            charset = part.get_content_charset() or "utf-8"
            body = payload.decode(charset, errors="replace")
            if content_type == "text/plain" and text_body is None:
                text_body = body
            elif content_type == "text/html" and html_body is None:
                html_body = body
    else:
        payload = message.get_payload(decode=True)
        if payload:
            charset = message.get_content_charset() or "utf-8"
            body = payload.decode(charset, errors="replace")
            if message.get_content_type() == "text/html":
                html_body = body
            else:
                text_body = body

    return text_body, html_body
