import streamlit as st
import requests
import os

# --- Page setup ---
st.set_page_config(page_title="Lyra AI 🚀", page_icon="🚀", layout="centered")

# --- Custom CSS for glow + buttons ---
st.markdown("""
    <style>
        .glow {
            font-size: 38px;
            text-align: center;
            color: #00FFFF;
            text-shadow: 0 0 10px #00FFFF, 0 0 20px #00FFFF, 0 0 30px #00FFFF;
        }
        .subtitle {
            text-align: center;
            color: #B0B0B0;
            font-size: 18px;
        }
        .stButton>button {
            background-color: #00BFFF;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 12px;
            font-size: 16px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #1E90FF;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<p class="glow">🚀 Lyra AI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your personal AI assistant powered by Llama 3.1 (Groq)</p>', unsafe_allow_html=True)

# --- Image Upload Section ---
st.markdown("### 📸 Upload an Image")
uploaded_file = st.file_uploader("Upload your image here", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

# --- Chat Section ---
st.markdown("### 💬 Ask Lyra Anything")
user_input = st.text_input("Type your question:")

if st.button("Ask 🚀"):
    if user_input:
        with st.spinner("Lyra is thinking..."):
            api_key = os.getenv("GROQ_API_KEY")  # Set this in Streamlit Secrets
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "llama-3.1-70b-versatile",  # ✅ Latest and best model
                "messages": [{"role": "user", "content": user_input}]
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
        st.warning("Please type something to ask Lyra!")
