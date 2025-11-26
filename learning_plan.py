import streamlit as st, datetime
def daily_plan():
    st.subheader("📅 Learning Plan for Today")
    st.write("• 20 SRS reviews")
    st.write("• 1 Graded reading")
    st.write("• 1 Speaking task")
    st.write("• 1 Writing task")
def schedule_review(days): return datetime.date.today()+datetime.timedelta(days=days)