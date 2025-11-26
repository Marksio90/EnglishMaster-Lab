# speech_module.py

import os
import streamlit as st

# --- dla TTS ---
try:
    from TTS.api import TTS
    tts = TTS(model_name="tts_models/en/jenny/jenny")  # możesz wybrać inny model
except ImportError:
    tts = None

# --- dla ASR / Transkrypcji ---
try:
    import openai
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    openai.api_key = OPENAI_API_KEY
except ImportError:
    openai = None

def synthesize_text(text: str, temp_file: str = "temp_audio.wav") -> str:
    """Konwertuje tekst na mowę, zapisuje plik WAV, zwraca ścieżkę."""
    if not tts:
        st.error("TTS library not installed")
        return None
    tts.tts_to_file(text=text, file_path=temp_file)
    return temp_file

def transcribe_audio(audio_bytes) -> str:
    """Wysyła audio do Whisper / OpenAI i zwraca transkrypt — jeśli API jest skonfigurowane."""
    if not openai:
        st.error("OpenAI library not installed / API key missing")
        return ""
    # zapis audio_bytes do pliku tymczasowego
    tmp = "input_audio.wav"
    with open(tmp, "wb") as f:
        f.write(audio_bytes)
    # przesyłamy do API
    resp = openai.audio.transcriptions.create(
        model="whisper-1",
        file= open(tmp, "rb")
    )
    return resp["text"]

def main():
    st.title("🔊 English Learning – Speech Module")

    st.header("Text → Speech (TTS)")
    txt = st.text_area("Wpisz tekst do odsłuchania (EN):", height=120)
    if st.button("Speak / Odtwórz"):
        wav = synthesize_text(txt)
        if wav:
            audio_bytes = open(wav, "rb").read()
            st.audio(audio_bytes, format="audio/wav")

    st.markdown("---")

    st.header("Speech → Text (ASR / Transkrypcja)")
    st.write("Nagraj krótki fragment (poprzez przeglądarkę), a usługa rozpozna tekst.")

    audio_data = st.file_uploader("Upload / nagraj plik audio (wav/mp3):", type=["wav","mp3","m4a"])
    if audio_data is not None:
        result = transcribe_audio(audio_data.read())
        st.subheader("Transkrypt:")
        st.write(result)

if __name__ == '__main__':
    main()
