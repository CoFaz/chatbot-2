import streamlit as st
import requests

# FastAPI endpoint
FASTAPI_URL = "http://127.0.0.1:8000/"

# Function to send user input to FastAPI and get response
def get_response_from_backend(prompt):
    try:
        response = requests.post(FASTAPI_URL, params={"prompt": prompt})
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json().get("response", "Error: No response from backend")
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with backend: {e}")
        return "Error: Could not connect to the backend."

# Title of the app
st.title("🍯 Your Beekeeping Assistant 🐝")
st.write(
    "This is a simple beekeeper chatbot that helps you with all questions surrounding honey & bees."
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages in the chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Text input for user message
if prompt := st.chat_input("What is up?"):
    # Store and display the current prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the FastAPI backend
    response = get_response_from_backend(prompt)

    # Display the assistant's response and store it in session state
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
