"""Backward-compatible entrypoint for the SystemVerilog debugging agent.

Prefer importing from ``sv_debug`` in new code. This module keeps older
imports and the CLI working.
"""

from sv_debug import (  # noqa: F401
    TOOLS,
    check_common_lint_patterns,
    debug_systemverilog,
    demo_mode_enabled,
    explain_compiler_error,
    explain_x_propagation,
    has_api_key,
)

# Older name used by previous versions / Gemini tool lists
tools = TOOLS

__all__ = [
    "TOOLS",
    "check_common_lint_patterns",
    "debug_systemverilog",
    "demo_mode_enabled",
    "explain_compiler_error",
    "explain_x_propagation",
    "has_api_key",
    "tools",
]


if __name__ == "__main__":
    print("Paste simulator output, compiler error, or SystemVerilog source below.")
    print("(Type END on its own line when finished.)")
    print("")

    lines: list[str] = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    result = debug_systemverilog("\n".join(lines))
    print("\n=== DEBUGGING RESULT ===\n")
    print(result)
