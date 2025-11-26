import streamlit as st
def prompt_write(q): st.markdown("✍ **Writing Task**"); return st.text_area(q)