"""Sandboxed Python execution environment."""
import ast
import io
import sys
from typing import Tuple, Any

FORBIDDEN_MODULES = {"os", "subprocess", "shutil", "socket", "pty"}

class SafetyChecker(ast.NodeVisitor):
    def __init__(self):
        self.violations = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in FORBIDDEN_MODULES:
                self.violations.append(f"Forbidden import: {alias.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module in FORBIDDEN_MODULES:
            self.violations.append(f"Forbidden import from: {node.module}")
        self.generic_visit(node)

class SafeREPL:
    @classmethod
    def execute(cls, code: str) -> Tuple[bool, str, Any]:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax Error: {e}", None

        checker = SafetyChecker()
        checker.visit(tree)
        if checker.violations:
            return False, "; ".join(checker.violations), None

        # Execute in restricted environment
        safe_globals = {"__builtins__": {"print": print, "range": range, "len": len, "sum": sum, "min": min, "max": max}}
        safe_locals = {}
        old_stdout = sys.stdout
        redirected = io.StringIO()
        sys.stdout = redirected

        try:
            exec(code, safe_globals, safe_locals)
            output = redirected.getvalue()
            return True, output.strip(), safe_locals
        except Exception as e:
            return False, str(e), None
        finally:
            sys.stdout = old_stdout
