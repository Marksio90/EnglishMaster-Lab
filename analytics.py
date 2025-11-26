import streamlit as st, random
def show_stats(): st.subheader("📊 Your Progress"); for sk in ["Grammar","Vocab","Listening","Speaking","Writing"]: st.metric(sk, random.randint(40,90))
