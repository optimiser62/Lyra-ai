import streamlit as st
from groq import Groq
from st_audiorec import st_audiorec
import tempfile
import base64

# Initialize Groq client
client = Groq(api_key=st.secrets.get("GROQ_API_KEY", None))

# --- App UI ---
st.set_page_config(page_title="Lyra AI 🚀", page_icon="🚀", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: #00FFFF; text-shadow: 0 0 15px #00FFFF;'>🚀 Lyra AI</h1>
    <p style='text-align: center; color: #AAA;'>Your personal AI assistant powered by <b>Llama 3.2 (Groq)</b></p>
""", unsafe_allow_html=True)

st.divider()

# --- Image Upload Section ---
st.subheader("🖼️ Upload an Image")
uploaded_file = st.file_uploader("Drag and drop a file (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.success("✅ Image uploaded successfully!")

st.divider()

# --- Voice Input Section ---
st.subheader("🎙️ Voice Input")
audio_bytes = st_audiorec()

user_input = ""

if audio_bytes:
    st.success("🎧 Voice recorded successfully!")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        st.audio(temp_audio.name)
        user_input = "Voice input received (text transcription not yet implemented)."

st.divider()

# --- Text Input Section ---
st.subheader("💬 Ask Lyra Anything")
user_question = st.text_area("Type your question here:", placeholder="Ask me anything...")

# --- Combine Inputs ---
final_input = user_question or user_input

if st.button("🚀 Ask Lyra"):
    if not final_input:
        st.warning("Please enter a question or use voice input.")
    else:
        with st.spinner("Lyra is thinking... 🤔"):
            try:
                response = client.chat.completions.create(
                    model="llama-3.2-90b-text-preview",
                    messages=[{"role": "user", "content": final_input}],
                )
                answer = response.choices[0].message.content
                st.markdown(f"### 💡 Lyra Says:\n\n{answer}")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# --- Footer ---
st.markdown("""
    <hr>
    <p style='text-align:center; color:#888;'>✨ Lyra AI — powered by Groq Llama 3.2 ✨</p>
""", unsafe_allow_html=True)
