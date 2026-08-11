import sys
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from sv_agent import debug_systemverilog, demo_mode_enabled, has_api_key

st.set_page_config(
    page_title="SV Debug Agent",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Space+Grotesk:wght@500;600;700&family=Source+Sans+3:wght@400;500;600&display=swap');

      html, body, [class*="css"] {
        font-family: "Source Sans 3", "Segoe UI", sans-serif;
      }

      .stApp {
        background:
          radial-gradient(900px 420px at 0% 0%, rgba(15, 118, 110, 0.10) 0%, transparent 55%),
          radial-gradient(700px 380px at 100% 0%, rgba(30, 58, 95, 0.08) 0%, transparent 50%),
          #eef2f4;
      }

      .block-container {
        padding-top: 1.75rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1180px !important;
      }

      /* Hide Streamlit chrome that fights the composition */
      #MainMenu { visibility: hidden; }
      header[data-testid="stHeader"] { background: transparent; }
      footer { visibility: hidden; }
      .stDeployButton { display: none !important; }
      div[data-testid="stToolbar"] { display: none !important; }

      h1 {
        font-family: "Space Grotesk", "Source Sans 3", sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.025em !important;
        color: #1a2f3a !important;
        margin: 0.2rem 0 0.55rem 0 !important;
        font-size: clamp(1.55rem, 2.4vw, 1.9rem) !important;
        line-height: 1.15 !important;
      }

      h2, h3 {
        font-family: "Space Grotesk", "Source Sans 3", sans-serif !important;
        color: #102028 !important;
        letter-spacing: -0.02em !important;
      }

      .brand {
        font-family: "Space Grotesk", sans-serif;
        font-size: clamp(2.2rem, 4vw, 3rem);
        font-weight: 700;
        letter-spacing: -0.035em;
        color: #0f766e;
        margin: 0;
        line-height: 1.05;
      }

      .lede {
        color: #3a4f5c;
        font-size: 1.05rem;
        line-height: 1.45;
        margin: 0 0 1.4rem 0;
        max-width: 36rem;
      }

      .mode-line {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        font-size: 0.84rem;
        font-weight: 600;
        color: #0f5132;
        background: #d9f3e7;
        border: 1px solid #9fd9c0;
        border-radius: 999px;
        padding: 0.28rem 0.75rem;
        margin: 0 0 1.1rem 0;
      }

      .mode-line.live {
        color: #1e3a5f;
        background: #dce9f8;
        border-color: #a9c6e8;
      }

      .mode-dot {
        width: 0.45rem;
        height: 0.45rem;
        border-radius: 50%;
        background: #0f766e;
        display: inline-block;
      }

      .mode-line.live .mode-dot { background: #2563eb; }

      div[data-testid="stTextArea"] textarea {
        font-family: "IBM Plex Mono", Consolas, monospace !important;
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
        background: #0f171d !important;
        color: #e8eef3 !important;
        border: 1px solid #24333e !important;
        border-radius: 12px !important;
        min-height: 360px !important;
        padding: 1rem 1.1rem !important;
      }

      div[data-testid="stTextArea"] label {
        font-family: "Space Grotesk", sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        color: #1a2b36 !important;
      }

      div[data-testid="stTextArea"] {
        margin-bottom: 0.75rem;
      }

      .actions {
        display: flex;
        gap: 0.65rem;
        margin: 0.2rem 0 1.25rem 0;
      }

      .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-family: "Source Sans 3", sans-serif !important;
        min-height: 2.7rem !important;
      }

      .stButton > button[kind="primary"] {
        background: #0f766e !important;
        border: 1px solid #0f766e !important;
        color: #fff !important;
      }

      .stButton > button[kind="primary"]:hover {
        background: #0d9488 !important;
        border-color: #0d9488 !important;
      }

      .stButton > button[kind="secondary"] {
        background: #fff !important;
        border: 1px solid #b7c5d0 !important;
        color: #243845 !important;
      }

      .result-shell {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid #c5d2dc;
        border-radius: 14px;
        padding: 1.15rem 1.25rem 1.25rem;
        margin-top: 0.35rem;
      }

      .result-shell h3 {
        margin-top: 0 !important;
      }

      [data-testid="stSidebar"] {
        background: #f7fafb;
        border-right: 1px solid #d5e0e8;
      }

      [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
      }

      .side-brand {
        font-family: "Space Grotesk", sans-serif;
        font-weight: 700;
        font-size: 1.05rem;
        color: #0f766e;
        letter-spacing: -0.02em;
        margin: 0 0 1rem 0;
      }

      .side-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #5b7382;
        margin: 1.1rem 0 0.45rem 0;
      }

      .side-copy {
        color: #3d5361;
        font-size: 0.92rem;
        line-height: 1.45;
        margin: 0 0 0.7rem 0;
      }

      .side-tip {
        color: #3d5361;
        font-size: 0.9rem;
        line-height: 1.4;
        margin: 0 0 0.55rem 0;
        padding-left: 0.7rem;
        border-left: 2px solid #9fd9c0;
      }

      /* Sample buttons: full-width, quieter than primary CTA */
      [data-testid="stSidebar"] .stButton > button {
        background: #fff !important;
        border: 1px solid #c9d6e0 !important;
        color: #1f3340 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        font-weight: 500 !important;
        min-height: 2.35rem !important;
        margin-bottom: 0.35rem !important;
      }

      [data-testid="stSidebar"] .stButton > button:hover {
        border-color: #0f766e !important;
        color: #0f766e !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

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


def _init_state() -> None:
    if "debug_input" not in st.session_state:
        st.session_state.debug_input = EXAMPLES["Missing reset (X risk)"]
    if "result" not in st.session_state:
        st.session_state.result = None
    if "error" not in st.session_state:
        st.session_state.error = None


def _set_example(name: str) -> None:
    st.session_state.debug_input = EXAMPLES[name]
    st.session_state.result = None
    st.session_state.error = None


_init_state()
demo = demo_mode_enabled()

with st.sidebar:
    st.markdown('<p class="side-brand">SV Debug Agent</p>', unsafe_allow_html=True)

    st.markdown('<p class="side-label">Try a sample</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="side-copy">Load an example, then hit Debug.</p>',
        unsafe_allow_html=True,
    )
    for name in EXAMPLES:
        if st.button(name, key=f"sample_{name}", use_container_width=True):
            _set_example(name)
            st.rerun()

    st.markdown('<p class="side-label">Mode</p>', unsafe_allow_html=True)
    if demo:
        st.markdown(
            '<p class="side-copy">Demo mode is on. Diagnosis runs offline '
            "with built-in helpers — no API key required.</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="side-copy">For Gemini later: set DEMO_MODE=false and '
            "add GEMINI_API_KEY in your .env file.</p>",
            unsafe_allow_html=True,
        )
    elif has_api_key():
        st.markdown(
            '<p class="side-copy">Live Gemini mode is active using your API key.</p>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<p class="side-copy">No API key found. Add GEMINI_API_KEY to .env, '
            "or set DEMO_MODE=true.</p>",
            unsafe_allow_html=True,
        )

    st.markdown('<p class="side-label">Tips</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="side-tip">Start from the first unknown X in a sim log.</p>'
        '<p class="side-tip">Keep a few lines of context around compiler errors.</p>'
        '<p class="side-tip">Source plus the error together works best.</p>',
        unsafe_allow_html=True,
    )

# Main composition: brand → one headline → one sentence → mode → editor → actions
st.markdown('<p class="brand">SV Debug Agent</p>', unsafe_allow_html=True)
st.title("Debug SystemVerilog faster")
st.markdown(
    '<p class="lede">Paste HDL, a compiler error, or a sim log. '
    "Get a concrete explanation of what is wrong and how to fix it.</p>",
    unsafe_allow_html=True,
)

if demo:
    st.markdown(
        '<div class="mode-line"><span class="mode-dot"></span>Demo mode · offline helpers</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="mode-line live"><span class="mode-dot"></span>Live mode · Gemini</div>',
        unsafe_allow_html=True,
    )

st.text_area(
    "Paste code, compiler error, or sim log",
    height=380,
    key="debug_input",
    placeholder="module … / error: … / # time 20: q=x",
    label_visibility="collapsed",
)

action_cols = st.columns([1.15, 1, 4.5], gap="small")
with action_cols[0]:
    run = st.button("Debug", type="primary", use_container_width=True)
with action_cols[1]:
    clear = st.button("Clear", type="secondary", use_container_width=True)

if clear:
    st.session_state.debug_input = ""
    st.session_state.result = None
    st.session_state.error = None
    st.rerun()

if run:
    if not st.session_state.debug_input.strip():
        st.session_state.result = None
        st.session_state.error = (
            "Paste some SystemVerilog or an error first — or load a sample from the sidebar."
        )
    else:
        try:
            with st.spinner("Analyzing your SystemVerilog…"):
                st.session_state.result = debug_systemverilog(st.session_state.debug_input)
            st.session_state.error = None
        except ValueError as exc:
            st.session_state.result = None
            st.session_state.error = str(exc)
        except Exception as exc:  # noqa: BLE001 — surface unexpected API failures in UI
            st.session_state.result = None
            st.session_state.error = f"Something went wrong while debugging: {exc}"

if st.session_state.error:
    st.error(st.session_state.error)

if st.session_state.result:
    st.markdown('<div class="result-shell">', unsafe_allow_html=True)
    st.subheader("Debugging result")
    st.markdown(st.session_state.result)
    st.markdown("</div>", unsafe_allow_html=True)
