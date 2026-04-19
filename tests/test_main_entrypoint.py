import os
import subprocess
import sys
import unittest
from pathlib import Path


class MainEntrypointTests(unittest.TestCase):
    def test_main_runs_with_valid_env(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        env = os.environ.copy()
        env.update(
            {
                "IMAP_HOST": "imap.example.com",
                "IMAP_PORT": "993",
                "IMAP_USERNAME": "user@example.com",
                "IMAP_PASSWORD": "secret",
            }
        )

        proc = subprocess.run(
            [sys.executable, "main.py"],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )

        self.assertEqual(proc.returncode, 0)
        self.assertIn("MCP Email Service ready: healthy", proc.stdout)


if __name__ == "__main__":
    unittest.main()
