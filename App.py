import streamlit as st
import requests
import os

# Page setup
st.set_page_config(page_title="Lyra AI", page_icon="🚀", layout="centered")

# Sidebar navigation
with st.sidebar:
    st.title("🚀 Lyra AI")
    st.markdown("### Menu")
    option = st.radio("Select Option", ["Chat", "About", "Help", "Settings"])
    st.markdown("---")
    st.caption("Developed by Lyra Labs ⚡")

# Main content changes based on sidebar selection
if option == "Chat":
    st.markdown("<h1 style='text-align:center; color:#00FFFF;'>🚀 Lyra AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Your personal AI assistant powered by Groq</p>", unsafe_allow_html=True)

    user_input = st.text_input("Ask Lyra anything:")

    if st.button("Ask"):
        if user_input:
            with st.spinner("Lyra is thinking..."):
                headers = {
                    "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "llama3-70b-8192",
                    "messages": [{"role": "user", "content": user_input}]
                }

                response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
                if response.status_code == 200:
                    answer = response.json()["choices"][0]["message"]["content"]
                    st.success(answer)
                else:
                    st.error("Error: " + response.text)

elif option == "About":
    st.header("About Lyra AI")
    st.write("Lyra AI is a next-gen intelligent assistant powered by Groq models. It helps you learn, create, and explore through natural conversation.")

elif option == "Help":
    st.header("Help")
    st.write("If Lyra isn’t responding, please check your internet or API key. For feedback, contact: support@lyra.ai")

elif option == "Settings":
    st.header("Settings")
    st.write("More customization features coming soon!")
