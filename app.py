import streamlit as st
from PIL import Image
import openai

# API key from secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Load logo
logo = Image.open("assets/evenpal_logo.png")
st.set_page_config(page_title="EvenPal", page_icon=logo)

# Title and image
st.image(logo, width=70)
st.markdown("## EvenPal – Your AI Mental Health Buddy")

# Chat history setup
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You're EvenPal, a calm and supportive mental health assistant chatbot."}
    ]

# Display previous messages
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("How are you feeling today?")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("EvenPal is typing..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
        )
        reply = response.choices[0].message.content
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
