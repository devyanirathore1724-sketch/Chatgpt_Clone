import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import json
st.set_page_config(
    page_title="My ChatGPT Clone",
    page_icon="🤖",
    layout="centered"
)
st.set_page_config(
    page_title="My ChatGPT Clone",
    page_icon="🤖",
    layout="centered"
)

load_dotenv()
client=Groq(api_key = os.getenv("GROQ_API_KEY"))
def load_chat():
    if os.path.exists("chat_history.json"):
        with open("chat_history.json", "r") as file:
            return json.load(file)
    return []
def save_chat(messages):
    with open("chat_history.json", "w") as file:
        json.dump(messages, file, indent=4)

if "messages" not in st.session_state:
    st.session_state.messages = load_chat()

with st.sidebar:
    st.header("⚙️ Menu")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
        st.divider()

    st.write("### 🤖 Model")
    st.write("Llama 3.3 70B")

    st.divider()

    st.write("### 🛠️ Built With")
    st.write("🐍 Python")
    st.write("🎨 Streamlit")
    st.write("⚡ Groq API")

    st.divider()

    st.info("""
    ### 📌 Features
    ✅ Chat History
    ✅ AI Memory
    ✅ System Prompt
    ✅ Groq API
    """)

st.caption("🚀AI Assistant powered by Groq & Llama")

st.title("🤖 My Chatgpt Clone")
st.markdown("### 💬 Your Personal AI Assistant")
st.caption("Ask me anything about Python, AI, Coding, or General Knowledge.")
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
user_input=st.chat_input("Type Your Message...")
if user_input:
     st.session_state.messages.append({
    "role": "user",
    "content": user_input
})
     save_chat(st.session_state.messages)
     with st.spinner("🤔 AI is thinking..."):
        assistant_reply=""
        message_placeholder=st.empty()
        response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Always reply in simple Hinglish."
        }
    ] + st.session_state.messages,
        stream=True
)
        for chunk in response:
           if chunk.choices[0].delta.content:
            assistant_reply += chunk.choices[0].delta.content
            message_placeholder.markdown(assistant_reply)
        st.session_state.messages.append({
       "role": "assistant",
       "content": assistant_reply
})
        save_chat(st.session_state.messages)
        st.rerun()