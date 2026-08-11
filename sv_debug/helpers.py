"""Local SystemVerilog helper tools used by demo mode and Gemini tool-calling."""

from __future__ import annotations


def explain_x_propagation(context: str) -> str:
    """Explain what X-propagation means in simulation output and likely causes."""
    _ = context
    return (
        "X-propagation means a signal's value is unknown ('x') in simulation, usually because "
        "a flip-flop or register was never reset/initialized before being used, or a signal is "
        "read before it's ever driven. Once 'x' appears, it usually spreads forward through any "
        "logic that uses that signal (e.g. x + 1 = x), so the FIRST time 'x' appears in the log "
        "is the most important clue -- everything after that point is likely just downstream effect. "
        "Common causes: missing reset logic in an always_ff block, an uninitialized register, "
        "or a multiplexer/case statement with an unhandled default case."
    )


def explain_compiler_error(error_text: str) -> str:
    """Explain a common Icarus Verilog / SystemVerilog compiler error and how to fix it."""
    _ = error_text
    return (
        "Common Icarus Verilog compiler errors and fixes:\n"
        "- 'syntax error' near a line: usually a missing semicolon, missing 'end', or "
        "mismatched begin/end pairs on the line just before the reported line.\n"
        "- 'Unknown module type': the module name in an instantiation doesn't match any "
        "module definition, or that file wasn't included in the iverilog command.\n"
        "- 'Port ... is not a port of module': the port name used when instantiating "
        "doesn't match a port name declared in the module definition -- check for typos.\n"
        "- 'input port cannot be driven': something is trying to assign a value to an "
        "input port from inside the module, which isn't allowed -- inputs are read-only "
        "inside a module."
    )


def check_common_lint_patterns(source_snippet: str) -> str:
    """Check SystemVerilog source code for a few common issues."""
    issues: list[str] = []

    if "always_ff" in source_snippet and "reset" not in source_snippet.lower():
        issues.append(
            "An always_ff block was found with no visible 'reset' handling -- "
            "this is a common cause of X-propagation."
        )

    if "always @" in source_snippet:
        issues.append(
            "Found an old-style 'always @' block -- modern SystemVerilog style "
            "prefers 'always_ff' for flip-flops or 'always_comb' for combinational "
            "logic, since these catch more mistakes at compile time."
        )

    if not issues:
        issues.append("No obvious issues found by this simple pattern check.")

    return " ".join(issues)


TOOLS = [
    explain_x_propagation,
    explain_compiler_error,
    check_common_lint_patterns,
]
