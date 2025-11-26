import streamlit as st
def show_card(card):
    st.subheader(card["data"]["front"])
    if st.button("Show Answer"):
        st.write(card["data"]["back"])