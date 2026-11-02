"""Unit tests for SafeREPL."""
import unittest
from agent_repl_sandbox.repl import SafeREPL

class TestSafeREPL(unittest.TestCase):
    def test_safe_execution(self):
        ok, out, _ = SafeREPL.execute("print('Hello from Sandbox')")
        self.assertTrue(ok)
        self.assertEqual(out, "Hello from Sandbox")

    def test_forbidden_import_blocked(self):
        ok, msg, _ = SafeREPL.execute("import os\nos.system('dir')")
        self.assertFalse(ok)
        self.assertIn("Forbidden import: os", msg)

if __name__ == "__main__":
    unittest.main()
