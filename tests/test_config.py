import os
import unittest
from unittest.mock import patch

from config import load_imap_config_from_env
from errors import ConfigurationError


class ConfigTests(unittest.TestCase):
    def test_invalid_port_raises_configuration_error(self) -> None:
        env = {
            "IMAP_HOST": "imap.example.com",
            "IMAP_PORT": "not-a-number",
            "IMAP_USERNAME": "user@example.com",
            "IMAP_PASSWORD": "secret",
        }
        with patch.dict(os.environ, env, clear=False):
            with self.assertRaises(ConfigurationError) as ctx:
                load_imap_config_from_env()
        self.assertEqual(str(ctx.exception), "IMAP_PORT must be a valid integer")


if __name__ == "__main__":
    unittest.main()
