import streamlit as st
def show_user(u):
    import sqlite3
    st.metric("🔥 Streak", u[3]); st.metric("🕒 Minutes", u[4]);