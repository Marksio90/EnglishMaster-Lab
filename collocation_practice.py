import streamlit as st
def show_practice(it):
    for p,l,t in it:
        st.write(f"🔎 {p} | lvl {l} | {t}")
        a=st.text_input(f"Rewrite with collocation: {p}")
        if a and p.lower() not in a.lower(): st.warning("Try again!")