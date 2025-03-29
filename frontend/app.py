import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="AI Chatbot", layout="centered")

# Custom CSS for modern and advanced UI
st.markdown(
    """
    <style>
        /* Global Styles */
        body {
            background-color: #111;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #fff;
            padding: 30px;
            margin: 0;
            overflow-x: hidden;
            height: 100vh;
            position: relative;
        }

        /* Starry background */
        .stars {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('https://www.transparenttextures.com/patterns/BindingLight.png') repeat top center;
            animation: stars 200s linear infinite;
            z-index: -1;
        }

        @keyframes stars {
            0% { transform: translate(0, 0); }
            100% { transform: translate(0, 500px); }
        }

        /* Chatbox Container */
        .chat-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            justify-content: flex-start;
            margin-bottom: 30px;
            max-width: 600px;
            margin: 0 auto;
        }

        .chat-message {
            padding: 12px 18px;
            border-radius: 10px;
            margin-bottom: 16px;
            max-width: 80%;
            word-wrap: break-word;
            background-color: #ffffff;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }

        .user {
            background-color: #FF4081; /* Bright Pink */
            color: #ffffff;
            align-self: flex-start;
            margin-left: 20px;
            animation: userMessage 0.5s ease;
        }

        .assistant {
            background-color: #1E88E5; /* Bright Blue */
            color: #ffffff;
            align-self: flex-end;
            margin-right: 20px;
            animation: assistantMessage 0.5s ease;
        }

        /* Typing animation */
        @keyframes userMessage {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes assistantMessage {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Input box design */
        .stTextInput>div>div>input {
            background-color: #222;
            color: #fff;
            padding: 15px;
            border-radius: 25px;
            border: 2px solid #333;
            font-size: 16px;
            width: 100%;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        }

        .stTextInput>div>div>input:focus {
            outline: none;
            border-color: #FF4081;
        }

        /* Send Button */
        .stButton>button {
            background-color: #FF4081;
            color: #ffffff;
            font-weight: bold;
            padding: 12px 25px;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .stButton>button:hover {
            background-color: #F50057;
        }

        /* Clear Chat Button */
        .clear-chat-button {
            background-color: transparent;
            color: #FF4081;
            border: 2px solid #FF4081;
            border-radius: 50px;
            padding: 8px 24px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 20px;
        }

        .clear-chat-button:hover {
            background-color: #FF4081;
            color: #ffffff;
        }

        /* Footer Styling */
        footer {
            text-align: center;
            margin-top: 40px;
            font-size: 14px;
            color: #ccc;
        }

        footer a {
            color: #FF4081;
            text-decoration: underline;
        }

        /* Typing animation styling */
        .typing-indicator {
            display: inline-block;
            width: 50px;
            height: 6px;
            margin: 10px 0;
            background-color: #1E88E5;
            animation: typing 1.5s infinite;
            border-radius: 10px;
        }

        @keyframes typing {
            0% { width: 0; }
            50% { width: 50px; }
            100% { width: 0; }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.title("AI Chatbot 🤖")
st.write("Powered by Mistral:latest & Ollama")
st.write("Made by Shrey")

# Starry background
st.markdown('<div class="stars"></div>', unsafe_allow_html=True)

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages with animations
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant">{message["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# User input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message to the chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(f'<div class="chat-message user">{user_input}</div>', unsafe_allow_html=True)

    # Display typing indicator and assistant's response with smooth spinner
    with st.chat_message("assistant"):
        typing_indicator = st.empty()
        typing_indicator.markdown('<div class="typing-indicator"></div>', unsafe_allow_html=True)
        
        with st.spinner("Thinking..."):
            try:
                # Send a request to the backend API
                response = requests.post("http://127.0.0.1:8000/chat", json={"prompt": user_input})

                # Check if the response is valid
                if response.status_code == 200:
                    bot_response = response.json().get("response", "Sorry, I couldn't understand that.")
                else:
                    bot_response = f"Error: {response.status_code}. Please try again later."

            except requests.exceptions.RequestException as e:
                # Handle connection errors gracefully
                bot_response = f"Network error: {e}. Please ensure the backend is running."

            # Display the bot's response
            typing_indicator.empty()  # Remove the typing indicator
            st.markdown(f'<div class="chat-message assistant">{bot_response}</div>', unsafe_allow_html=True)

    # Append assistant message to the chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Button to clear chat history
if st.button("Clear Chat", key="clear_button", help="Clear the chat history", use_container_width=True):
    st.session_state.messages = []

# Footer with GitHub link
st.markdown(
    """
    <footer>
        <a href="https://github.com/your-repo-url" target="_blank">View Source on GitHub</a>
    </footer>
    """, 
    unsafe_allow_html=True
)
