import streamlit as st
import requests
import os

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="Lyra AI", layout="wide")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_TEXT = "llama-3.2-11b-text"
MODEL_VISION = "llama-3.2-90b-vision-preview"

# ---------------------- STYLES ----------------------
st.markdown("""
<style>
    body { background-color: #0d0d0d; }
    .chat-container { max-width: 750px; margin: auto; padding: 20px; }
    .user-bubble {
        background: #005eff; padding: 12px 16px; border-radius: 18px;
        color: white; margin: 10px 0; max-width: 80%; float: right; clear: both;
    }
    .ai-bubble {
        background: #1f1f1f; padding: 12px 16px; border-radius: 18px;
        color: white; margin: 10px 0; max-width: 80%; float: left; clear: both;
    }
    .bottom-bar {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: #0d0d0d; padding: 15px;
        border-top: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- CHAT HISTORY ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# ---------------------- DISPLAY CHAT ----------------------
for msg in st.session_state.messages:
    bubble = "user-bubble" if msg["role"] == "user" else "ai-bubble"
    st.markdown(f"<div class='{bubble}'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- INPUT AREA ----------------------
st.markdown("<div class='bottom-bar'>", unsafe_allow_html=True)

uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
uploaded_audio = st.file_uploader("Upload Audio", type=["wav", "mp3"])

text_input = st.text_input("Ask Lyra...", label_visibility="collapsed")
send = st.button("Send 🚀")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- PROCESS REQUEST ----------------------
def call_groq(messages, model):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {"model": model, "messages": messages}

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers, json=data
    )
    
    return response.json()

# ---------------------- AUDIO → TEXT ----------------------
def speech_to_text(audio_file):
    files = {"file": (audio_file.name, audio_file.read(), audio_file.type)}
    response = requests.post(
        "https://api.groq.com/openai/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        files=files
    )
    return response.json()["text"]

# ---------------------- SEND MESSAGE ----------------------
if send:
    final_input = text_input

    # ✅ If audio uploaded → convert to text
    if uploaded_audio:
        final_input += "\n(Audio → Text: " + speech_to_text(uploaded_audio) + ")"

    # ✅ If image uploaded → convert to vision message
    if uploaded_image:
        img_bytes = uploaded_image.read()
        st.session_state.messages.append({
            "role": "user",
            "content": f"[Uploaded Image: {uploaded_image.name}]"
        })

        vision_msg = [
            {"role": "user", "content": [
                {"type": "text", "text": final_input},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_bytes.hex()}"}
            ]}
        ]
        ai_res = call_groq(vision_msg, MODEL_VISION)
    else:
        # ✅ Text-only message
        st.session_state.messages.append({"role": "user", "content": final_input})
        ai_res = call_groq(st.session_state.messages, MODEL_TEXT)

    try:
        ai_text = ai_res["choices"][0]["message"]["content"]
    except:
        ai_text = "⚠️ Error: " + str(ai_res)

    st.session_state.messages.append({"role": "assistant", "content": ai_text})
    st.rerun()
