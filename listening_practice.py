import streamlit as st
def show_listening(item):
    lid, title, level, topic, script = item
    st.markdown(f"### 🎧 {title} (Level {level})")
    st.write(f"**Topic:** {topic}")
    st.write("---")
    st.write(script)

def comprehension_quiz(lid, script):
    st.subheader("🧠 Comprehension Quiz")
    q1 = st.text_input("1. What is the main idea?")
    q2 = st.text_input("2. List one key detail")
    if st.button("Submit Answers"):
        if not q1 or not q2:
            st.error("Fill all answers ✋"); return None
        st.success("Answers submitted! ✅")
        return {"main":q1, "detail":q2}