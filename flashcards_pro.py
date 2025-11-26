import streamlit as st
def card(front, back):
    st.info(front)
    if st.button(f"Show: {front}"):
        st.write(back)