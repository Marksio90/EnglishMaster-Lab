import streamlit as st, sqlite3
from stories_db import init_stories, add_story
from stories_generator import gen_story
init_stories()
def show_story():
    s=gen_story()
    st.subheader(f"📖 {s['title']} ({s['tone']})")
    st.write(s["story"])
    if st.button("Save this story to learning journal"):
        add_story(1,s["title"],s["story"],s["cefr"],s["tone"]); st.success("✅ Saved!")