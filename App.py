import os
import streamlit as st
from groq import Groq

# --- Setup ---
st.set_page_config(page_title="Lyra AI", page_icon="🤖", layout="centered")

# --- Title ---
st.markdown("<h1 style='text-align: center; color: cyan;'>🤖 Lyra AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your personal AI assistant powered by Groq</p>", unsafe_allow_html=True)

# --- API Setup ---
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("🚨 API key not found! Please set your GROQ_API_KEY in environment variables.")
else:
    client = Groq(api_key=api_key)

    # --- Input ---
    user_input = st.text_area("💬 Ask Lyra AI anything:", placeholder="Type your question here...")

    # --- Submit Button ---
    if st.button("✨ Ask"):
        if not user_input.strip():
            st.warning("Please enter a question before submitting.")
        else:
            try:
                with st.spinner("Lyra is thinking... 🤔"):
                    response = client.chat.completions.create(
                        model="llama3-8b",  # ✅ Correct model name
                        messages=[{"role": "user", "content": user_input}]
                    )
                    reply = response.choices[0].message.content
                    st.markdown("### 🧠 Lyra’s Answer:")
                    st.success(reply)

            except Exception as e:
                st.error(f"⚠️ Error: {e}")

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size: 12px;'>Built with ❤️ by Aditya | Powered by Groq</p>", unsafe_allow_html=True)
