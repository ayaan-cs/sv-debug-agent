"""SystemVerilog debugging agent package."""

from .config import demo_mode_enabled, has_api_key
from .helpers import (
    TOOLS,
    check_common_lint_patterns,
    explain_compiler_error,
    explain_x_propagation,
)
from .pipeline import debug_systemverilog
from .samples import SAMPLES, get_sample
from .suggestions import suggest_alternatives

__all__ = [
    "SAMPLES",
    "TOOLS",
    "check_common_lint_patterns",
    "debug_systemverilog",
    "demo_mode_enabled",
    "explain_compiler_error",
    "explain_x_propagation",
    "get_sample",
    "has_api_key",
    "suggest_alternatives",
]
