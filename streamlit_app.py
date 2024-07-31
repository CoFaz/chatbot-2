import streamlit as st
from openai import OpenAI
import requests

FASTAPI_URL = "http://127.0.0.1:8000/"
# Show title and description.
st.title("🍯 Your Beekeeping assistant 🐝")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

def get_response_from_backend(prompt):
    try:
        response = requests.post(FASTAPI_URL, json={"prompt": prompt})
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with backend: {e}")
        return "Error: Could not connect to the backend."

if "messages" not in st.session_state:
    st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
     with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = get_response_from_backend(prompt)

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
