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
# ✅ SESSION STATE
# ==============================
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ==============================
# ✅ IMAGE UPLOAD
# ==============================
st.subheader("Upload an image")
uploaded = st.file_uploader("Upload JPG/PNG", type=["jpg","jpeg","png"])

image_message = None

if uploaded:
    img_bytes = uploaded.read()
    encoded_image = base64.b64encode(img_bytes).decode()

    image_message = {
        "role": "user",
        "content": [
            {"type":"text", "text":"Here is the image"},
            {"type":"input_image", "image": encoded_image}
        ]
    }

# ==============================
# ✅ Chat history display
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
# ✅ BOTTOM BAR
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

col1, col2 = st.columns([6,1])

with col1:
    user_input = st.text_input("Type here...", key="input", label_visibility="collapsed")

with col2:
    send = st.button("🚀 Send")

st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# ✅ SEND HANDLER
# ==============================
if send and user_input.strip():

    # Add user text to history
    st.session_state["messages"].append({"role":"user","content":user_input})

    # BUILD API PAYLOAD
    payload_messages = st.session_state["messages"].copy()

    # Add image if uploaded
    if image_message:
        payload_messages.append(image_message)

    payload = {
        "model": "llama-3.2-11b-text",
        "messages": payload_messages
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers
        ).json()

        # ✅ FIX: safe check for choices
        if "choices" not in response:
            st.session_state["messages"].append({
                "role": "assistant",
                "content": "Groq error: " + str(response)
            })
        else:
            reply =
