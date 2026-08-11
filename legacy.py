"""
Legacy one-file Streamlit app + SystemVerilog debugging agent.

Preserved as a single runnable snapshot of the original agent + Streamlit UI.
Prefer the desktop app under ui/app/ for day-to-day use.

Run from the repo root:
    streamlit run legacy.py
"""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Config (legacy sv_agent behavior)
# ---------------------------------------------------------------------------

load_dotenv(Path(__file__).resolve().parent / ".env")

_PLACEHOLDER_KEYS = {
    "",
    "your_gemini_api_key_here",
    "your_api_key_here",
}


def _api_key() -> str | None:
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def has_api_key() -> bool:
    key = _api_key()
    return bool(key and key.strip() not in _PLACEHOLDER_KEYS)


def demo_mode_enabled() -> bool:
    raw = os.getenv("DEMO_MODE")
    if raw is not None:
        return raw.strip().lower() in {"1", "true", "yes", "on"}
    return not has_api_key()


def _require_api_key() -> str:
    key = _api_key()
    if not key or key.strip() in _PLACEHOLDER_KEYS:
        raise ValueError(
            "Missing Gemini API key. Open .env and replace your_gemini_api_key_here "
            "with a real key from https://aistudio.google.com/apikey "
            "or keep DEMO_MODE=true."
        )
    return key.strip()


# ---------------------------------------------------------------------------
# Agent helpers (original sv_agent tools)
# ---------------------------------------------------------------------------


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


tools = [
    explain_x_propagation,
    explain_compiler_error,
    check_common_lint_patterns,
]


def _demo_debug_systemverilog(user_input: str) -> str:
    """Local offline diagnosis using the same helper tools (no Gemini call)."""
    text = user_input.strip()
    lower = text.lower()
    sections: list[str] = [
        "**Demo mode** — this response was generated locally without calling Gemini.",
        "",
    ]

    if any(token in lower for token in ("unknown", "'x'", "x-prop")) or (
        "x" in lower and ("time" in lower or "reset" in lower or "data" in lower)
    ):
        sections.extend(["### X-propagation", explain_x_propagation(text), ""])

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
        sections.extend(["### Compiler / simulator errors", explain_compiler_error(text), ""])

    if "module" in lower or "always" in lower or "assign" in lower or len(sections) <= 2:
        sections.extend(["### Quick lint check", check_common_lint_patterns(text), ""])

    if len(sections) <= 2:
        sections.append(
            "No strong X-propagation or compiler-error keywords were detected. "
            "Try a sample below, or paste a real compile/sim log."
        )

    sections.extend(
        [
            "---",
            "To use the full Gemini agent, set DEMO_MODE=false in .env and add a real "
            "GEMINI_API_KEY from https://aistudio.google.com/apikey.",
        ]
    )
    return "\n".join(sections)


def debug_systemverilog(user_input: str) -> str:
    """Diagnose SystemVerilog input via demo helpers or Gemini (legacy agent)."""
    if demo_mode_enabled():
        return _demo_debug_systemverilog(user_input)

    client = genai.Client(api_key=_require_api_key())
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
        config=types.GenerateContentConfig(tools=tools),
    )
    return response.text


# ---------------------------------------------------------------------------
# Samples
# ---------------------------------------------------------------------------

EXAMPLES = {
    "Missing reset (X risk)": """\
module counter (
  input  logic clk,
  input  logic en,
  output logic [3:0] count
);
  always_ff @(posedge clk) begin
    if (en)
      count <= count + 1;
  end
endmodule""",
    "Old-style always block": """\
module toggle (
  input  wire clk,
  output reg  q
);
  always @(posedge clk) begin
    q <= ~q;
  end
endmodule""",
    "Compiler syntax error": """\
tb.v:12: syntax error
I give up.
error: Unable to elaborate top level modules""",
    "X in simulation log": """\
# time 0: reset=x data=x
# time 10: reset=0 data=x
# time 20: q=x (first unknown observed here)
# time 30: out=x""",
}


# ---------------------------------------------------------------------------
# Legacy Streamlit UI
# ---------------------------------------------------------------------------


def run_streamlit_ui() -> None:
    st.set_page_config(
        page_title="SV Debug Agent (Legacy)",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.title("SystemVerilog Debugging Agent")
    st.caption("Legacy Streamlit UI + agent in one file. Prefer ui/app for the desktop app.")

    if demo_mode_enabled():
        st.info("Demo mode is on — offline helpers, no API key required.")
    elif has_api_key():
        st.success("Live Gemini mode — using your local API key.")
    else:
        st.warning("No API key found. Set DEMO_MODE=true or add GEMINI_API_KEY in .env.")

    st.write(
        "Paste your SystemVerilog code, simulator output, or compiler error below."
    )

    with st.sidebar:
        st.header("Samples")
        choice = st.selectbox("Load a sample", list(EXAMPLES.keys()))
        if st.button("Load sample", use_container_width=True):
            st.session_state["debug_input"] = EXAMPLES[choice]

    if "debug_input" not in st.session_state:
        st.session_state["debug_input"] = EXAMPLES["Missing reset (X risk)"]

    debug_input = st.text_area(
        "SystemVerilog Code / Error",
        height=300,
        key="debug_input",
    )

    col_a, col_b = st.columns(2)
    with col_a:
        run = st.button("Debug", type="primary", use_container_width=True)
    with col_b:
        clear = st.button("Clear", use_container_width=True)

    if clear:
        st.session_state["debug_input"] = ""
        st.rerun()

    if run:
        if not debug_input.strip():
            st.warning("Please paste some SystemVerilog code or an error first.")
        else:
            try:
                with st.spinner("Analyzing your SystemVerilog..."):
                    result = debug_systemverilog(debug_input)
                st.subheader("Debugging Result")
                st.markdown(result)
            except ValueError as exc:
                st.error(str(exc))
            except Exception as exc:  # noqa: BLE001
                st.error(f"Something went wrong while debugging: {exc}")


# Streamlit sets __name__ to "__main__" when running this file.
if __name__ == "__main__":
    run_streamlit_ui()
