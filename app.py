import streamlit as st
from openai import OpenAI
from PIL import Image

# Load your logo
logo = Image.open("assets/evenpal_logo.png")  # Make sure this image exists in /assets

# Set Streamlit page config
st.set_page_config(page_title="EvenPal - Mental Health Companion", page_icon=logo)

# Custom CSS
st.markdown("""
    <style>
        .stButton > button {
            background-color: #5f9ea0;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff;
            color: #000000;
        }
        .message {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Title and logo
col1, col2 = st.columns([1, 5])
with col1:
    st.image(logo, width=70)
with col2:
    st.markdown("## EvenPal – Your AI Mental Health Buddy")

# Set up OpenAI client
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You're EvenPal, a calm and supportive mental health assistant chatbot."}
    ]

# Display chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("How are you feeling today?")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("EvenPal is typing..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
        )
        reply = response.choices[0].message.content
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
