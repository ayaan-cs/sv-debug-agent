import streamlit as st
from sv_agent import debug_systemverilog


st.title("SystemVerilog Debugging Agent")

st.write(
    "Paste your SystemVerilog code, simulator output, "
    "or compiler error below."
)

debug_input = st.text_area(
    "SystemVerilog Code / Error",
    height=300
)


if st.button("Debug"):
    if not debug_input.strip():
        st.warning("Please paste some SystemVerilog code or an error first.")
    else:
        with st.spinner("Analyzing your SystemVerilog..."):
            result = debug_systemverilog(debug_input)

        st.subheader("Debugging Result")
        st.write(result)
