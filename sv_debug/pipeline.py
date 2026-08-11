"""Route debug requests to demo helpers or Gemini."""

from __future__ import annotations

from .config import demo_mode_enabled
from .demo import demo_debug_systemverilog
from .gemini import gemini_debug_systemverilog


def debug_systemverilog(
    user_input: str,
    *,
    include_alternatives_markdown: bool = True,
) -> str:
    """Diagnose SystemVerilog input via demo helpers or Gemini."""
    if demo_mode_enabled():
        return demo_debug_systemverilog(
            user_input,
            include_alternatives_markdown=include_alternatives_markdown,
        )
    return gemini_debug_systemverilog(user_input)
