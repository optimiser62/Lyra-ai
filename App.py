import os
import streamlit as st
import requests

st.set_page_config(page_title="Lyra AI", page_icon="🤖", layout="centered")

st.title("✨ Lyra AI")
st.markdown("Your personal intelligent assistant, powered by **Llama 3 via Groq** 🧠")

groq_api_key = st.text_input("Enter your Groq API key:", type="password")

user_input = st.text_input("Ask Lyra anything:")

if st.button("Ask"):
    if user_input and groq_api_key:
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
