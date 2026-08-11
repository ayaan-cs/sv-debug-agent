"""Lightweight input classifiers for demo diagnosis / suggestions."""

from __future__ import annotations

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
