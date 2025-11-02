import streamlit as st
import requests
import sounddevice as sd
import wavio
import tempfile
import os
from groq import Groq

# ---- SETUP ----
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

# ---- RECORD AUDIO FUNCTION ----
def record_audio(duration=5, samplerate=44100):
    st.info("🎤 Recording... Speak now!")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    st.success("✅ Recording complete!")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wavio.write(temp_file.name, audio, samplerate, sampwidth=2)
    return temp_file.name

# ---- STREAMLIT UI ----
st.set_page_config(page_title="Lyra AI", page_icon="🤖", layout="wide")

st.markdown(
    """
    <h1 style='text-align:center; color:#00FFFF; text-shadow:0 0 20px #00FFFF;'>💠 Lyra AI</h1>
    <p style='text-align:center;'>Ask anything, speak your question, or upload a photo!</p>
    """,
    unsafe_allow_html=True
)

# ---- SIDEBAR ----
st.sidebar.title("⚙️ Options")
mode = st.sidebar.radio("Choose Input Type:", ["💬 Text", "🎙️ Voice", "🖼️ Photo"])

# ---- TEXT INPUT ----
if mode == "💬 Text":
    user_input = st.text_input("Type your question:")
    if st.button("Ask"):
        if user_input.strip():
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="llama-3.2-90b-text-preview",
                    messages=[{"role": "user", "content": user_input}]
                )
            st.markdown("### 💡 Lyra says:")
            st.write(response.choices[0].message.content)
        else:
            st.warning("Please enter a question.")

# ---- VOICE INPUT ----
elif mode == "🎙️ Voice":
    if st.button("🎧 Record Voice"):
        audio_file = record_audio()
        st.audio(audio_file)

        # You could add transcription using Whisper API here later

# ---- PHOTO UPLOAD ----
elif mode == "🖼️ Photo":
    uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Photo", use_container_width=True)
        st.success("✅ Image uploaded successfully!")
        # Later, you can connect this to AI vision analysis using Groq or Gemini

st.markdown(
    """
    <hr>
    <p style='text-align:center; color:gray;'>✨ Lyra AI — Intelligent. Simple. Fast.</p>
    """,
    unsafe_allow_html=True
)
