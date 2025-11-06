# ------------------------------------------
# ✅ FIXED CHATGPT-STYLE INPUT BAR (Bottom)
# ------------------------------------------

st.markdown("""
<style>
.input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 15px;
    background-color: #0d0d0d;
    border-top: 1px solid #333;
}
input[type="text"] {
    border-radius: 10px;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])

    with col1:
        user_input = st.text_input(
            "Type your message...",
            value=voice_text if voice_text else "",
            label_visibility="collapsed",
            key="user_msg"
        )

    with col2:
        send = st.button("🚀", key="send_btn")

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# ✅ SEND MESSAGE TO GROQ
# ------------------------------------------
if send and user_input.strip() != "":
    st.session_state["messages"].append({"role": "user", "content": user_input})

    payload = {
        "model": "llama-3.2-11b-text",
        "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]]
    }

    if encoded_image:
        payload["messages"].append({
            "role": "user",
            "content": "Here is an image.",
            "image": encoded_image
        })

    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        json=payload,
        headers=headers
    )

    reply = response.json()["choices"][0]["message"]["content"]

    st.session_state["messages"].append({"role": "assistant", "content": reply})

    st.rerun()
