import streamlit as st
import requests
import base64
import os

# ==============================
# ✅ PAGE CONFIG
# ==============================
st.set_page_config(page_title="Lyra AI", layout="wide")

# ==============================
# ✅ TITLE
# ==============================
st.markdown("""
<h1 style="text-align:center; color:#00eaff;">
🚀 Lyra AI
</h1>
<p style="text-align:center; font-size:20px; color:#ccc;">
Hi, I'm Lyra! How can I help you today?
</p>
""", unsafe_allow_html=True)

# ==============================
# ✅ SESSION STATE (chat history)
# ==============================
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

# ==============================
# ✅ IMAGE UPLOAD
# ==============================
st.subheader("Upload an image")
uploaded = st.file_uploader("Upload JPG/PNG", type=["jpg", "jpeg", "png"])

encoded_image = None
if uploaded:
    img_bytes = uploaded.read()
    encoded_image = base64.b64encode(img_bytes).decode()

# ==============================
# ✅ SHOW CHAT HISTORY (CHATGPT STYLE)
# ==============================
st.markdown("<hr>", unsafe_allow_html=True)

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='text-align:right; background:#1e1e1e; padding:10px; margin:5px; border-radius:10px; color:white;'>{msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align:left; background:#0f0f0f; padding:10px; margin:5px; border-radius:10px; color:#00eaff;'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

# ==============================
# ✅ BOTTOM INPUT BAR (CHATGPT STYLE)
# ==============================
st.markdown("""
<style>
.bottom-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 15px;
    background: #000;
    border-top: 1px solid #333;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='bottom-bar'>", unsafe_allow_html=True)

col1, col2 = st.columns([6, 1])

with col1:
    user_input = st.text_input("Type here...", key="input", label_visibility="collapsed")

with col2:
    send = st.button("🚀 Send")

st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# ✅ HANDLE SEND
# ==============================
if send and user_input.strip():

    # Add user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    payload = {
        "model": "llama-3.2-11b-text",
        "messages": st.session_state["messages"]
    }

    # Add image if uploaded
    if encoded_image:
        payload["messages"].append({
            "role": "user",
            "content": "Here is the image.",
            "image": encoded_image
        })

    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers
        )

        reply = response.json()["choices"][0]["message"]["content"]

        st.session_state["messages"].append({"role": "assistant", "content": reply})

    except Exception as e:
        st.session_state["messages"].append({"role": "assistant", "content": "Error: " + str(e)})

    st.rerun()
