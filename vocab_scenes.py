import streamlit as st
def contextual_list(it):
    st.subheader("Contextual Vocabulary Practice")
    for uid,item,t,d in it:
        st.write(f"📘 {item} ({t}) – review today")