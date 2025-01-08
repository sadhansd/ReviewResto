import streamlit as st
from collections import OrderedDict

# Predefined chatbot responses
def chatbot_response(user_input):
    responses = {
        "hi": "Hello! How can I help you?",
        "hello": "Hi there! What can I assist you with?",
        "how are you": "I'm just a program, but I'm here to help!",
        "bye": "Goodbye! Have a great day!",
    }
    return responses.get(user_input.lower(), "I'm sorry, I didn't understand that.")

# App title
st.title("Main App Content")

# Initialize session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []  # Store chat history

# Sidebar for chatbot
with st.sidebar:
    st.header("Chatbot")
    user_input = st.chat_input("Type your message here...")
    if user_input:

        bot_response = chatbot_response(user_input)
        chat = [{"role": "user", "content": user_input},{"role": "assistant", "content": bot_response}]
        st.session_state.messages.append(chat)

    chat_container = st.container()
    with chat_container:
        for chat in reversed(st.session_state.messages):
            st.chat_message(chat[0]['role'], avatar="🧑").markdown(chat[0]['content'])
            with st.container(border=True):
                st.chat_message(chat[1]['role'], avatar="🤖").markdown(chat[1]['content'])

        
