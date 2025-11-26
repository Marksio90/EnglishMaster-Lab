import streamlit as st
def record_audio():
    st.header("Record Speaking Sample")
    audio = st.audio_input("Press to speak")
    if audio is not None:
        return audio
    return None
