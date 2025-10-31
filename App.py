import os
import streamlit as st
from groq import Groq

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Streamlit UI
st.set_page_config(page_title="Lyra AI", page_icon="🚀", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: white; font-size: 48px; text-shadow: 0 0 25px cyan;'>🚀 Lyra AI</h1>
    <h3 style='text-align: center; color: gray;'>Your personal AI assistant powered by Groq</h3>
""", unsafe_allow_html=True)

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Ask Lyra anything:", placeholder="Type your question here...")

if st.button("Ask", use_container_width=True):
    if user_input:
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # ✅ Updated working model
                messages=[
                    {"role": "system", "content": "You are Lyra, a friendly and smart AI assistant."},
                    {"role": "user", "content": user_input},
                ]
            )
            reply = completion.choices[0].message.content

            # Store chat history
            st.session_state.history.append(("You", user_input))
            st.session_state.history.append(("Lyra", reply))

        except Exception as e:
            reply = f"Error: {str(e)}"
            st.session_state.history.append(("Error", reply))

# Display chat history
st.markdown("---")
for sender, message in st.session_state.history:
    color = "cyan" if sender == "You" else "white"
    if sender == "Error":
        color = "red"
    st.markdown(f"<p style='color: {color};'><b>{sender}:</b> {message}</p>", unsafe_allow_html=True)

# Background styling
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    div.stButton > button {
        background-color: #0078ff;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        box-shadow: 0 0 20px cyan;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 30px cyan;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)
