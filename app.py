import streamlit as st

from sv_agent import debug_systemverilog, demo_mode_enabled, has_api_key

st.set_page_config(
    page_title="SV Debug Agent",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Visual direction: cool slate workspace, teal accent — readable for long HDL logs.
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Source+Sans+3:wght@400;600;700&display=swap');

      html, body, [class*="css"] {
        font-family: "Source Sans 3", "Segoe UI", sans-serif;
      }

      .stApp {
        background:
          radial-gradient(1200px 600px at 10% -10%, #d7e8e4 0%, transparent 55%),
          radial-gradient(900px 500px at 100% 0%, #e8eef5 0%, transparent 50%),
          linear-gradient(180deg, #f3f6f8 0%, #e9eef2 100%);
      }

      .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1100px;
      }

      h1, h2, h3 {
        letter-spacing: -0.02em;
        color: #14212b !important;
      }

      .hero-kicker {
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #0f766e;
        margin-bottom: 0.35rem;
      }

      .hero-sub {
        color: #3d5160;
        font-size: 1.05rem;
        margin: 0 0 1.25rem 0;
        max-width: 42rem;
        line-height: 1.45;
      }

      .status-pill {
        display: inline-block;
        padding: 0.28rem 0.7rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.85rem;
      }

      .status-demo {
        background: #ecfdf5;
        color: #065f46;
        border: 1px solid #a7f3d0;
      }

      .status-live {
        background: #eff6ff;
        color: #1e3a8a;
        border: 1px solid #bfdbfe;
      }

      .hint-row {
        color: #4b6070;
        font-size: 0.92rem;
        margin: 0.25rem 0 0.75rem 0;
      }

      div[data-testid="stTextArea"] textarea {
        font-family: "IBM Plex Mono", Consolas, monospace !important;
        font-size: 0.92rem !important;
        line-height: 1.45 !important;
        background: #101820 !important;
        color: #e7eef4 !important;
        border: 1px solid #2a3b49 !important;
        border-radius: 10px !important;
      }

      div[data-testid="stTextArea"] label {
        font-weight: 600 !important;
        color: #1b2a36 !important;
      }

      .result-panel {
        background: #ffffffcc;
        border: 1px solid #c9d5df;
        border-radius: 12px;
        padding: 1rem 1.15rem;
        box-shadow: 0 8px 24px rgba(20, 33, 43, 0.06);
      }

      .stButton > button[kind="primary"] {
        background: #0f766e !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.2rem !important;
      }

      .stButton > button[kind="primary"]:hover {
        background: #0d9488 !important;
      }

      [data-testid="stSidebar"] {
        background: #f7fafb;
        border-right: 1px solid #d5e0e8;
      }

      [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #14212b !important;
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


def _load_example() -> None:
    choice = st.session_state.get("example_choice")
    if choice and choice in EXAMPLES:
        st.session_state.debug_input = EXAMPLES[choice]
        st.session_state.result = None
        st.session_state.error = None


_init_state()
demo = demo_mode_enabled()

with st.sidebar:
    st.markdown("### How to use")
    st.markdown(
        "1. Paste HDL, a compile error, or a sim log  \n"
        "2. Or load a sample below  \n"
        "3. Click **Debug**"
    )

    st.selectbox(
        "Load a sample",
        options=list(EXAMPLES.keys()),
        key="example_choice",
        on_change=_load_example,
    )

    st.divider()
    st.markdown("### Mode")
    if demo:
        st.success("Demo mode is on — no API key needed.")
        st.caption(
            "Diagnosis uses built-in SystemVerilog helpers. "
            "Set `DEMO_MODE=false` and a real `GEMINI_API_KEY` in `.env` for Gemini."
        )
    elif has_api_key():
        st.info("Live Gemini mode — using your API key.")
    else:
        st.warning(
            "No API key found. Add `GEMINI_API_KEY` to `.env`, "
            "or set `DEMO_MODE=true`."
        )

    st.divider()
    st.markdown("### Tips")
    st.markdown(
        "- Paste the **first** `'x'` in a sim log — later X's are often just fallout  \n"
        "- Include a few lines of context around compiler errors  \n"
        "- Source + error together usually gives a clearer answer"
    )

st.markdown('<div class="hero-kicker">SV Debug Agent</div>', unsafe_allow_html=True)
st.title("Debug SystemVerilog faster")
st.markdown(
    '<p class="hero-sub">'
    "Paste source, Icarus/Verilator errors, or simulation logs. "
    "Get a concrete explanation of what is wrong and how to fix it."
    "</p>",
    unsafe_allow_html=True,
)

if demo:
    st.markdown(
        '<span class="status-pill status-demo">Demo mode · offline helpers</span>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<span class="status-pill status-live">Live mode · Gemini</span>',
        unsafe_allow_html=True,
    )

st.markdown(
    '<p class="hint-row">Use a monospace paste area below — samples are in the sidebar.</p>',
    unsafe_allow_html=True,
)

st.text_area(
    "SystemVerilog code, compiler error, or sim log",
    height=320,
    key="debug_input",
    placeholder="Paste your module, error message, or waveform/log excerpt here…",
)

col_run, col_clear, _ = st.columns([1.2, 1, 4])
with col_run:
    run = st.button("Debug", type="primary", use_container_width=True)
with col_clear:
    clear = st.button("Clear", use_container_width=True)

if clear:
    st.session_state.debug_input = ""
    st.session_state.result = None
    st.session_state.error = None
    st.rerun()

if run:
    if not st.session_state.debug_input.strip():
        st.session_state.result = None
        st.session_state.error = "Paste some SystemVerilog code or an error first — or load a sample from the sidebar."
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
    st.subheader("Debugging result")
    st.markdown('<div class="result-panel">', unsafe_allow_html=True)
    st.markdown(st.session_state.result)
    st.markdown("</div>", unsafe_allow_html=True)
