import streamlit as st
import requests
import os

# ✅ Page settings
st.set_page_config(page_title="Lyra AI", layout="wide")

# ✅ ChatGPT-style centered layout
st.markdown("""
<style>
.chat-container {
    max-width: 700px;
    margin: auto;
    padding: 20px;
}
.message-user {
    background-color: #1f2937;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
    color: white;
}
.message-ai {
    background-color: #0ea5e9;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
    color: black;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🚀 Lyra AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Your personal AI assistant powered by Groq</p>", unsafe_allow_html=True)

# ✅ Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Show chat history
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    role_class = "message-user" if msg["role"] == "user" else "message-ai"
    st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ✅ User input
user_input = st.text_input("Ask Lyra anything:")

# ✅ API Key
groq_key = os.getenv("GROQ_API_KEY")

if st.button("Send 🚀"):
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama-3.2-11b-text",   # ✅ Latest working model
            "messages": st.session_state.messages
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.experimental_rerun()
        else:
            st.error("Error: " + response.text)
