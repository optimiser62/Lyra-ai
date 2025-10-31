import os
import streamlit as st
import requests

# --- Setup page ---
st.set_page_config(page_title="Lyra AI", page_icon="🤖", layout="centered")

# --- Custom Styling ---
st.markdown("""
    <style>
        body {
            background-color: #0E1117;
            color: white;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
            background-color: #1A1D24;
            color: white;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            font-size: 16px;
            padding: 8px 20px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .chat-bubble-user {
            background-color: #2B313E;
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 10px;
            color: white;
        }
        .chat-bubble-bot {
            background-color: #1E90FF;
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 10px;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.title("✨ Lyra AI")
st.markdown("Your personal intelligent assistant powered by **Llama 3.1 via Groq** 🧠")

# --- API Key from environment ---
groq_api_key = os.getenv("GROQ_API_KEY")

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- User Input ---
user_input = st.text_input("Ask Lyra anything:")

if st.button("Ask"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": user_input}]
        }

        with st.spinner("Lyra is thinking..."):
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data
            )

        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error("Error: " + response.text)

# --- Show Chat Messages ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'><b>Lyra:</b> {msg['content']}</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("💡 Built by **Aditya Raj** using [Groq API](https://groq.com) and Streamlit")
