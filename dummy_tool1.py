# dummy_tool1.py

import streamlit as st
import openai

def run():
    st.title("🤖 AI Chatbot")
    st.caption("🚀 Chat with an AI assistant powered by your secret API key.")

    # ----------------------------------------------------------------------------
    # 1) Initialize the OpenAI client using helper
    # ----------------------------------------------------------------------------
    from model_utils import get_openai_client
    client = get_openai_client()

    # ----------------------------------------------------------------------------
    # 2) Initialize or retrieve conversation history
    # ----------------------------------------------------------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi there! How can I help you today?"}
        ]

    # ----------------------------------------------------------------------------
    # 3) Clear Chat button
    # ----------------------------------------------------------------------------
    if st.button("🗑️ Clear Chat"):
        # Reset to initial assistant greeting
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi there! How can I help you today?"}
        ]

    # ----------------------------------------------------------------------------
    # 4) Model selection (fixed at top of page)
    # ----------------------------------------------------------------------------
    from model_utils import get_available_models
    model_options = get_available_models(client)

    if model_options:
        selected_model = st.selectbox("Choose a model:", model_options)
    else:
        st.warning("⚠️ No active models found in LM Studio. Please enter model ID manually:")
        selected_model = st.text_input("Model ID:", value="meta-llama/Llama-3.3-70B-Instruct")

    # ----------------------------------------------------------------------------
    # 5) Display existing conversation using chat bubbles
    # ----------------------------------------------------------------------------
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # ----------------------------------------------------------------------------
    # 6) Handle new user input with st.chat_input()
    # ----------------------------------------------------------------------------
    prompt = st.chat_input("Type your message...")
    if prompt:
        # Append and show user's message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Call the API and show a spinner while waiting
        with st.spinner("AI is thinking..."):
            try:
                # Filter out initial greeting if it starts with an assistant message (strict Jinja template compliance)
                api_messages = st.session_state.messages
                if api_messages and api_messages[0]["role"] == "assistant":
                    api_messages = api_messages[1:]

                response = client.chat.completions.create(
                    model=selected_model,
                    messages=api_messages,
                )
                assistant_msg = response.choices[0].message.content
            except Exception as e:
                assistant_msg = f"Error: {e}"

        # Append and display the assistant's reply
        st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
        st.chat_message("assistant").write(assistant_msg)
