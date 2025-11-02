import os
import streamlit as st
import requests
import speech_recognition as sr

# --- Page setup ---
st.set_page_config(page_title="Lyra AI", page_icon="🚀", layout="centered")

st.markdown("""
    <h1 style='text-align:center; color:#00FFFF; text-shadow:0 0 10px #00FFFF;'>🚀 Lyra AI</h1>
    <p style='text-align:center; color:#FFFFFF;'>Your futuristic AI assistant powered by <b>Llama 3.2 🧠</b></p>
""", unsafe_allow_html=True)

# --- Store chat history ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Voice recording ---
def record_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Listening… Speak now!")
        audio = r.listen(source, phrase_time_limit=10)
    try:
        text = r.recognize_google(audio)
        st.success(f"🗣 You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I couldn’t understand that.")
        return None
    except sr.RequestError:
        st.error("Speech recognition service error.")
        return None

# --- User input ---
st.write("### Type or speak your question to Lyra:")
col1, col2 = st.columns([3, 1])
with col1:
    user_input = st.text_input("Your message:", key="user_text")
with col2:
    if st.button("🎤 Speak"):
        spoken = record_voice()
        if spoken:
            user_input = spoken

# --- Ask Lyra ---
if st.button("🚀 Ask Lyra"):
    if user_input:
        with st.spinner("Lyra is thinking…"):
            headers = {
                "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "llama-3.2-90b-text",   # ✅ Llama 3.2 model
                "messages": [{"role": "user", "content": user_input}]
            }
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers, json=data
            )

            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                st.session_state.history.append(("You", user_input))
                st.session_state.history.append(("Lyra", answer))
                st.success(answer)
            else:
                st.error("Error: " + response.text)
    else:
        st.warning("Please type or speak something first!")

# --- Chat history display ---
st.markdown("### 💬 Chat History")
for role, text in st.session_state.history:
    if role == "You":
        st.markdown(f"🧍‍♂️ **{role}:** {text}")
    else:
        st.markdown(f"🤖 **{role}:** {text}")
