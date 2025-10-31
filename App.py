import streamlit as st
import requests
import os

# ✅ Page setup
st.set_page_config(page_title="Lyra AI", page_icon="🚀", layout="centered")

# ✅ Custom CSS for glowing theme
st.markdown("""
    <style>
        body {
            background-color: #0a0a0a;
            color: white;
            text-align: center;
        }
        .title {
            font-size: 3em;
            font-weight: bold;
            color: #00eaff;
            text-shadow: 0 0 20px #00eaff;
        }
        .subtitle {
            color: #cccccc;
            font-size: 1.2em;
        }
        .stButton>button {
            background: linear-gradient(90deg, #00eaff, #0077ff);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            font-size: 1em;
            box-shadow: 0 0 20px #00eaff;
            transition: 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 30px #00eaff;
        }
        .stTextInput>div>div>input {
            background-color: #111111;
            color: white;
            border: 1px solid #00eaff;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Title Section
st.markdown("<h1 class='title'>🚀 Lyra AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your personal AI assistant powered by Groq</p>", unsafe_allow_html=True)

# ✅ User Input
user_input = st.text_input("Ask Lyra anything:")

# ✅ API Key (from environment variable)
api_key = os.getenv("GROQ_API_KEY")

# ✅ Button and API Call
if st.button("Ask"):
    if user_input:
        with st.spinner("Lyra is thinking..."):
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            # ✅ Updated Model (latest supported one)
            data = {
                "model": "llama-3.1-70b-versatile",
                "messages": [{"role": "user", "content": user_input}]
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                st.success(answer)
            else:
                st.error(f"Error: {response.text}")
