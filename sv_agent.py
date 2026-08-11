import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).resolve().parent / ".env")

_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
_PLACEHOLDER_KEYS = {
    "",
    "your_gemini_api_key_here",
    "your_api_key_here",
}


def demo_mode_enabled() -> bool:
    """Return True when DEMO_MODE is on (default: on when no real API key is set)."""
    raw = os.getenv("DEMO_MODE")
    if raw is not None:
        return raw.strip().lower() in {"1", "true", "yes", "on"}
    return not has_api_key()


def has_api_key() -> bool:
    """Return True when a non-placeholder Gemini API key is configured."""
    return bool(_api_key and _api_key.strip() not in _PLACEHOLDER_KEYS)


def _get_client() -> genai.Client:
    """Build a Gemini client, failing clearly if the API key is missing."""
    if not has_api_key():
        raise ValueError(
            "Missing Gemini API key. Open the .env file in this project and replace "
            "your_gemini_api_key_here with a real key from https://aistudio.google.com/apikey "
            "or keep DEMO_MODE=true to try the app without a key."
        )
    return genai.Client(api_key=_api_key.strip())


def explain_x_propagation(context: str) -> str:
    """Explain what X-propagation means in simulation output and likely causes."""
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
    issues = []

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
        issues.append(
            "No obvious issues found by this simple pattern check."
        )

    return " ".join(issues)


tools = [
    explain_x_propagation,
    explain_compiler_error,
    check_common_lint_patterns,
]


def _demo_debug_systemverilog(user_input: str) -> str:
    """Local, offline diagnosis using the same helper tools (no Gemini call)."""
    text = user_input.strip()
    lower = text.lower()

    sections: list[str] = [
        "**Demo mode** — this response was generated locally without calling Gemini.",
        "",
    ]

    if "x" in lower or "unknown" in lower or "'x'" in lower or "x-prop" in lower:
        sections.append("### X-propagation")
        sections.append(explain_x_propagation(text))
        sections.append("")

    if any(
        token in lower
        for token in (
            "syntax error",
            "unknown module",
            "is not a port",
            "cannot be driven",
            "error:",
            "iverilog",
        )
    ):
        sections.append("### Compiler / simulator errors")
        sections.append(explain_compiler_error(text))
        sections.append("")

    if "module" in lower or "always" in lower or "assign" in lower:
        sections.append("### Quick lint check")
        sections.append(check_common_lint_patterns(text))
        sections.append("")

    if len(sections) <= 2:
        sections.append("### Quick lint check")
        sections.append(check_common_lint_patterns(text))
        sections.append("")
        sections.append(
            "No strong X-propagation or compiler-error keywords were detected. "
            "Try one of the sample inputs in the sidebar, or paste a real compile/sim log."
        )

    sections.append("---")
    sections.append(
        "To use the full Gemini agent, set `DEMO_MODE=false` in `.env` and add a real "
        "`GEMINI_API_KEY` from https://aistudio.google.com/apikey."
    )
    return "\n".join(sections)


def debug_systemverilog(user_input: str) -> str:
    """Diagnose SystemVerilog input via demo helpers or Gemini."""
    if demo_mode_enabled():
        return _demo_debug_systemverilog(user_input)

    client = _get_client()

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=(
            "A SystemVerilog/FPGA engineer needs help debugging this:\n\n"
            f"{user_input}\n\n"
            "Use your available tools to check for known issues, then give a "
            "clear, concrete explanation of what's likely wrong and how to fix it. "
            "If possible, identify the likely line or section causing the issue. "
            "If nothing looks wrong, say so plainly."
        ),
        config=types.GenerateContentConfig(
            tools=tools,
        ),
    )

    return response.text


if __name__ == "__main__":
    print("Paste simulator output, compiler error, or SystemVerilog source below.")
    print("(Type END on its own line when finished.)")
    print("")

    lines = []

    while True:
        line = input()

        if line.strip() == "END":
            break

        lines.append(line)

    user_input = "\n".join(lines)

    result = debug_systemverilog(user_input)

    print("\n=== DEBUGGING RESULT ===\n")
    print(result)
