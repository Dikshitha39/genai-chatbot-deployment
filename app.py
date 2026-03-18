import streamlit as st
from groq import Groq
import os

# Page config
st.set_page_config(
    page_title="GenAI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 GenAI Chatbot")
st.caption("Powered by Groq LLaMA3 — Built by Dikshitha")

# Get API key
api_key = os.environ.get("GROQ_API_KEY", "")
if not api_key:
    api_key = st.text_input(
        "Enter your Groq API Key",
        type="password",
        placeholder="gsk_..."
    )

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    if not api_key:
        st.error("Please enter your Groq API key!")
    else:
        # Add user message
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        with st.chat_message("user"):
            st.write(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content
                st.write(reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )
