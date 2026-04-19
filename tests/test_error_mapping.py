import unittest

from errors import IMAPAuthenticationError, to_mcp_error


class ErrorMappingTests(unittest.TestCase):
    def test_maps_domain_error_to_structured_payload(self) -> None:
        payload = to_mcp_error(IMAPAuthenticationError("IMAP authentication failed"))
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["code"], "imap_authentication_error")
        self.assertEqual(payload["error"]["message"], "IMAP authentication failed")


if __name__ == "__main__":
    unittest.main()
