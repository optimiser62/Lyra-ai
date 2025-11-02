import streamlit as st
import requests
from PIL import Image
import io
import os

# --- Page Setup ---
st.set_page_config(page_title="Lyra AI", page_icon="🚀", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: #00ffff; text-shadow: 0 0 15px #00ffff;'>
        🚀 Lyra AI
    </h1>
    <p style='text-align: center; color: white;'>
        Your personal AI assistant powered by Llama 3.2 (Groq)
    </p>
""", unsafe_allow_html=True)

st.markdown("---")

# --- API Key (Stored Secretly in Code or Environment) ---
api_key = os.getenv("GROQ_API_KEY") or "YOUR_GROQ_API_KEY_HERE"

if not api_key or api_key == "YOUR_GROQ_API_KEY_HERE":
    st.error("❌ Please set your Groq API key in the code or environment variable 'GROQ_API_KEY'.")
else:
    # --- Chat History ---
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --- Image Upload ---
    st.subheader("📸 Upload an Image (Optional)")
    uploaded_file = st.file_uploader("Drag and drop or select an image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

    st.markdown("---")

    # --- Chat Interface ---
    st.subheader("💬 Ask Lyra Anything")

    user_input = st.text_input("Type your question:")

    if st.button("Ask", use_container_width=True):
        if user_input.strip() == "":
            st.warning("Please enter a question.")
        else:
            try:
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_input})

                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

                # Prepare conversation context
                data = {
                    "model": "llama-3.2-70b-text-preview",
                    "messages": st.session_state.chat_history
                }

                response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

                if response.status_code == 200:
                    result = response.json()
                    ai_message = result["choices"][0]["message"]["content"]

                    # Add AI reply to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_message})

                    # Display conversation
                    for msg in st.session_state.chat_history:
                        if msg["role"] == "user":
                            st.markdown(f"🧑‍💻 **You:** {msg['content']}")
                        else:
                            st.markdown(f"🤖 **Lyra:** {msg['content']}")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Error: {e}")

    # --- Footer ---
    st.markdown("---")
    st.markdown("<p style='text-align:center; color:gray;'>✨ Powered by Groq & Llama 3.2</p>", unsafe_allow_html=True)
