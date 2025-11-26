import streamlit as st
def nav(u=None): st.sidebar.title("EnglishMaster"); return st.sidebar.selectbox("Mode",["Learn","SRS","Stats"])
def metric_block(l): st.metric("Level",l)
