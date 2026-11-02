"""Command line interface for agent-repl-sandbox."""
from .repl import SafeREPL

def main():
    ok, out, _ = SafeREPL.execute("x = sum([1, 2, 3, 4])\nprint('Sum:', x)")
    print("Safe REPL execution:", ok, "
Stdout:", out)

if __name__ == "__main__":
    main()
