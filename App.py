import streamlit as st
import requests

# Streamlit page setup
st.set_page_config(page_title="Lyra AI", page_icon="🤖", layout="centered")

st.title("✨ Lyra AI")
st.markdown("Your personal intelligent assistant, powered by **Llama 3.1 via Groq** 🧠")

# Input for Groq API Key (so it's never hardcoded in your code)
groq_api_key = st.text_input("Enter your Groq API key:", type="password")

# User question
user_input = st.text_input("Ask Lyra anything:")

# When the user clicks 'Ask'
if st.button("Ask"):
    if not groq_api_key:
        st.warning("⚠️ Please enter your Groq API key first.")
    elif not user_input:
        st.warning("⚠️ Please enter a question for Lyra.")
    else:
        with st.spinner("Lyra is thinking... 🤔"):
            headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "user", "content": user_input}
                ]
            }

            # Send request to Groq API
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data
            )

            # Show response or error
            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                st.success(answer)
            else:
                st.error("Error: " + response.text)
