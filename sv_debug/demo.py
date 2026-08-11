"""Offline demo diagnosis — no Gemini / no API key required."""

from __future__ import annotations

from .helpers import (
    check_common_lint_patterns,
    explain_compiler_error,
    explain_x_propagation,
)

_COMPILER_HINTS = (
    "syntax error",
    "unknown module",
    "is not a port",
    "cannot be driven",
    "error:",
    "iverilog",
)


def looks_like_x_issue(text: str) -> bool:
    lower = text.lower()
    return any(token in lower for token in ("unknown", "'x'", "x-prop", " =x", "=x", "x ")) or (
        "x" in lower and ("time" in lower or "reset" in lower or "data" in lower)
    )


def looks_like_compiler_issue(text: str) -> bool:
    lower = text.lower()
    return any(token in lower for token in _COMPILER_HINTS)


def looks_like_source(text: str) -> bool:
    lower = text.lower()
    return any(token in lower for token in ("module", "always", "assign"))


def demo_debug_systemverilog(user_input: str) -> str:
    """Local diagnosis using the same helper tools (no Gemini call)."""
    text = user_input.strip()

    sections: list[str] = [
        "**Demo mode** — this response was generated locally without calling Gemini.",
        "",
    ]

    matched = False

    if looks_like_x_issue(text):
        matched = True
        sections.append("### X-propagation")
        sections.append(explain_x_propagation(text))
        sections.append("")

    if looks_like_compiler_issue(text):
        matched = True
        sections.append("### Compiler / simulator errors")
        sections.append(explain_compiler_error(text))
        sections.append("")

    if looks_like_source(text) or not matched:
        sections.append("### Quick lint check")
        sections.append(check_common_lint_patterns(text))
        sections.append("")

    if not matched and not looks_like_source(text):
        sections.append(
            "No strong X-propagation or compiler-error keywords were detected. "
            "Try one of the sample inputs, or paste a real compile/sim log."
        )

    sections.append("---")
    sections.append(
        "To use the full Gemini agent, set DEMO_MODE=false in .env and add a real "
        "GEMINI_API_KEY from https://aistudio.google.com/apikey."
    )
    return "\n".join(sections)
