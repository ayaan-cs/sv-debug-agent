"""SystemVerilog debugging agent package.

Public entry points stay stable via ``sv_agent`` and ``sv_debug``.
"""

from .config import demo_mode_enabled, has_api_key
from .helpers import (
    check_common_lint_patterns,
    explain_compiler_error,
    explain_x_propagation,
    TOOLS,
)
from .pipeline import debug_systemverilog
from .samples import SAMPLES, get_sample

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
]
