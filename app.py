import streamlit as st
from story_practice_ui import show_story
st.title("Story Mode Reading + Journal")
if st.button("Generate Story"):
    show_story()