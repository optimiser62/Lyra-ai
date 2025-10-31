 import streamlit as st
from groq import Groq
import os

# ----------------- SETUP -----------------
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

st.set_page_config(page_title="Lyra AI", page_icon="✨", layout="centered")

# ----------------- CUSTOM STYLING -----------------
st.markdown("""
    <style>
        body {
            background-color: #0E1117;
        }
        .title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #ffffff;
            text-shadow: 0 0 15px #00ffcc;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #cfcfcf;
        }
        .stButton>button {
            background-color: #00ffcc;
            color: black;
            border: none;
            border-radius: 8px;
            padding: 10px 25px;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.2s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #00e6b8;
            transform: scale(1.05);
        }
        .footer {
            text-align: center;
            font-size: 15px;
            color: #00ffcc;
            margin-top: 40px;
            text-shadow: 0 0 8px #00ffcc;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- APP HEADER -----------------
st.markdown("<div class='title'>✨ Lyra AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your personal AI assistant powered by Llama 3.1 via Groq 🧠</div>", unsafe_allow_html=True)
st.write("")

# ----------------- USER INPUT -----------------
prompt = st.text_input("Ask Lyra anything:")

if st.button("Ask"):
    if prompt:
        with st.spinner("Lyra is thinking... 🤔"):
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192"
            )
            st.markdown(f"**Lyra:** {chat_completion.choices[0].message.content}")
    else:
        st.warning("Please type something to ask Lyra!")

# ----------------- FOOTER -----------------
st.markdown(
    """
    <div class='footer'>
        🚀 Powered by <b>Lyra AI</b>
    </div>
    """,
    unsafe_allow_html=True
)   
