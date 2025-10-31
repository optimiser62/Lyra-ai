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

    # --- Initialize chat history ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- Display chat history ---
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        color = "#00FFFF" if role == "assistant" else "#FFFFFF"
        bg = "#0A0A0A" if role == "assistant" else "#1C1C1C"
        st.markdown(
            f"<div style='background-color:{bg}; padding:12px; border-radius:10px; "
            f"margin-bottom:8px; box-shadow:0 0 12px {color}; color:white;'>"
            f"<b>{'Lyra' if role=='assistant' else 'You'}:</b> {content}</div>",
            unsafe_allow_html=True
        )

    # --- Input box ---
    user_input = st.text_input("💬 Type your message:", placeholder="Ask something...")

    # --- Button style ---
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

    # --- Handle chat ---
    if st.button("Send"):
        if not user_input.strip():
            st.warning("Please enter a message.")
        else:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})

            try:
                with st.spinner("💭 Lyra is thinking..."):
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=st.session_state.messages
                    )
                    reply = response.choices[0].message.content

                    # Add AI reply
                    st.session_state.messages.append({"role": "assistant", "content": reply})

                    # Force rerun to show updated chat
                    st.rerun()
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
