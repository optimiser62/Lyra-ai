import streamlit as st
import base64
import requests
import speech_recognition as sr
import os

# ------------------------------------------
# ✅ PAGE CONFIG
# ------------------------------------------
st.set_page_config(page_title="Lyra AI", page_icon="🚀", layout="wide")

# Hide Streamlit menu + sidebar
hide_st = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st, unsafe_allow_html=True)

# ------------------------------------------
# ✅ WELCOME HEADER (ChatGPT Style)
# ------------------------------------------
if "messages" not in st.session_state or len(st.session_state["messages"]) == 0:
    st.markdown("""
    <div style="text-align:center; margin-top: 40px; margin-bottom: 20px;">
        <h1 style="
            font-size: 45px;
            font-weight: 800;
            background: linear-gradient(90deg, #00eaff, #00ffa2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        ">
            🚀 Lyra AI
        </h1>
        <p style="color:#e0e0e0; font-size: 22px;">
            Hi, I'm Lyra! How can I help you today?
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <h1 style="text-align:center; color:white; margin-top:20px;">🚀 Lyra AI</h1>
    """, unsafe_allow_html=True)

# ------------------------------------------
# ✅ SESSION STATE FOR CHAT
# ------------------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ------------------------------------------
# ✅ IMAGE UPLOAD
# ------------------------------------------
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

encoded_image = None
if uploaded_image:
    img_bytes = uploaded_image.read()
    encoded_image = base64.b64encode(img_bytes).decode("utf-8")
    st.image(img_bytes, caption="Uploaded Image", width=250)

# ------------------------------------------
# ✅ VOICE INPUT SECTION
