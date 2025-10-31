import os
import streamlit as st
from groq import Groq

# --- Page setup ---
st.set_page_config(page_title="Lyra AI", page_icon="🚀", layout="centered")

# --- Glowing Title ---
st.markdown("""
    <h1 style='text-align: center;
               color: #00FFFF;
               text-shadow: 0 0 25px #00FFFF;
               font-family: "Poppins", sans-serif;'>
        🚀 Lyra AI
    </h1>
    <p style='text-align: center; color: #CCCCCC;'>
        Your personal AI assistant powered by Groq
    </p>
""", unsafe_allow_html=True)

# --- API Setup ---
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("🚨 API key not found! Please set your GROQ_API_KEY in environment variables.")
else:
    client = Groq(api_key=api_key)

    # --- Input box ---
    user_input = st.text_input("💬 Ask Lyra anything:", placeholder="Type your question here...")

    # --- Button Glow Style ---
    st.markdown("""
        <style>
            div.stButton > button:first-child {
                background-color: #00FFFF;
                color: black;
                border-radius: 12px;
                font-weight: bold;
                font-size: 16px;
                box-shadow: 0px 0px 15px #00FFFF;
                transition: 0.3s;
            }
            div.stButton > button:first-child:hover {
                background-color: #00CCCC;
                box-shadow: 0px 0px 25px #00FFFF;
                transform: scale(1.05);
            }
        </style>
    """, unsafe_allow_html=True)

    # --- Ask Button ---
    if st.button("Ask"):
        if not user_input.strip():
            st.warning("Please enter a question before submitting.")
        else:
            try:
                with st.spinner("💭 Lyra is thinking..."):
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",  # ✅ updated working model
                        messages=[{"role": "user", "content": user_input}]
                    )
                    reply = response.choices[0].message.content
                    st.markdown(
                        f"<div style='background-color:#0A0A0A; padding:15px; border-radius:10px; "
                        f"box-shadow:0 0 20px #00FFFF; color:white;'>{reply}</div>",
                        unsafe_allow_html=True
                    )
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
