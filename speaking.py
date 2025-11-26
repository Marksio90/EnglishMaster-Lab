import streamlit as st
def prompt_speaking(q):
    st.markdown("🎤 **Speaking Task**")
    st.write(q)
    st.button("Start Recording (future voice streaming 0-file mode)")