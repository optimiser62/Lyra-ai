import os
import streamlit as st
import requests

groq_api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Lyra AI", page_icon="🤖", layout="centered")
st.title("✨ Lyra AI")
st.markdown("Your personal intelligent assistant, powered by **Llama 3.1 via Groq** 🧠")

user_input = st.text_input("Ask Lyra anything:")

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
                    # 🔹 Updated model name
                    "model": "llama-3.1-8b-instant",
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
