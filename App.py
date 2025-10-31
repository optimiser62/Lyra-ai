import os
import streamlit as st
import requests

# ✅ Get API key securely from environment variable
groq_api_key = os.getenv("GROQ_API_KEY")

# 🧠 Streamlit App Setup
st.set_page_config(page_title="Lyra AI", page_icon="🤖", layout="centered")
st.title("✨ Lyra AI")
st.markdown("Your personal intelligent assistant, powered by **Llama 3 via Groq** 🧠")

# 🔹 User input
user_input = st.text_input("Ask Lyra anything:")

# 🔹 Button to send question
if st.button("Ask"):
    if user_input:
        if not groq_api_key:
            st.error("⚠️ API key not found. Please add it in Streamlit Secrets or environment variables.")
        else:
            with st.spinner("Lyra is thinking..."):
                headers = {
                    "Authorization": f"Bearer {groq_api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "llama3-8b-8192",
                    "messages": [
                        {"role": "user", "content": user_input}
                    ]
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
                    st.error("Error: " + response.text)
    else:
        st.warning("Please enter a question before asking.")
