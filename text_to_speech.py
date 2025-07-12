import streamlit as st
import requests
import urllib.parse

TOKEN = "AwU-Ivx5HdLjFZur"

VOICE_OPTIONS = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
LANG_OPTIONS = {
    "English": "E",
    "Chinese": "C",
    "Spanish": "S",
    "French": "F",
    "German": "G"
}

def generate_speech(message: str, lang_code: str, voice: str) -> bytes | None:
    """Call the Pollinations TTS API and return audio bytes."""
    text = f"Read the following in {lang_code}: {message}"
    encoded_text = urllib.parse.quote(text)
    url = f"https://text.pollinations.ai/{encoded_text}?token={TOKEN}"
    params = {"model": "openai-audio", "voice": voice}

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        if 'audio/mpeg' in response.headers.get('Content-Type', ''):
            return response.content
    except requests.RequestException as e:
        st.error(f"Request error: {e}")
    return None

def run():
    st.title("🗣️ Text to Speech")
    st.caption("Convert text into spoken audio using Pollinations TTS service.")

    message = st.text_area("Enter text:", height=150)
    lang = st.selectbox("Language:", list(LANG_OPTIONS.keys()))
    voice = st.selectbox("Voice:", VOICE_OPTIONS)

    if st.button("Generate Audio"):
        if not message.strip():
            st.warning("Please enter some text.")
            return
        with st.spinner("Generating audio..."):
            audio_bytes = generate_speech(message.strip(), LANG_OPTIONS[lang], voice)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mpeg")
            st.download_button("Download Audio", audio_bytes, file_name="speech.mp3")
        else:
            st.error("Failed to generate audio.")
