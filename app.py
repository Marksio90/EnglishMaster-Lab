import streamlit as st
from error_memory import init_error_db
from error_classifier import classify
from error_review import show_errors
init_error_db()
st.title("Error Memory Panel")
inp = st.text_input("Type mistake sample")
if st.button("Save Error"):
    tag = classify(inp)
    from error_memory import save_error
    save_error(1, inp, tag)
    st.success("Saved!")
if st.button("Show Errors"):
    show_errors()