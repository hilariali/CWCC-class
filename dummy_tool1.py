# dummy_tool1.py

import streamlit as st
import openai

def run():
    st.title("🤖 AI Chatbot (Dummy Tool 1)")
    st.caption("🚀 A Streamlit chatbot powered by your chosen LLM")

    # ----------------------------------------------------------------------------
    # 1) Sidebar: Show API key field
    # ----------------------------------------------------------------------------
    with st.sidebar:
        st.text_input(
            "OpenAI API Key", 
            key="chatbot_api_key", 
            type="password", 
            help="Enter your OpenAI API key (or a compatible endpoint key)."
        )
        st.write("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
        st.write(
            "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        )

    # ----------------------------------------------------------------------------
    # 2) Model selection (keep this at the top of main area)
    # ----------------------------------------------------------------------------
    model_options = [
        "DeepSeek-R1-0528",
        "Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
        "Qwen3-235B-A22B-FP8",
    ]
    selected_model = st.selectbox("Choose a model:", model_options)

    # ----------------------------------------------------------------------------
    # 3) Initialize conversation history in session_state
    # ----------------------------------------------------------------------------
    if "messages" not in st.session_state:
        # Start with a greeting from the assistant
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi there! How can I help you today?"}
        ]

    # ----------------------------------------------------------------------------
    # 4) Display existing conversation using chat_message bubbles
    # ----------------------------------------------------------------------------
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # ----------------------------------------------------------------------------
    # 5) Handle new user input with st.chat_input()
    # ----------------------------------------------------------------------------
    prompt = st.chat_input("Type your message...")
    if prompt:
        if not st.session_state.chatbot_api_key:
            st.info("🔑 Please add your OpenAI API key in the sidebar to continue.")
            st.stop()

        # Append the user's message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Initialize the new OpenAI client (v1.0.0+)
        client = openai.OpenAI(
            api_key=st.session_state.chatbot_api_key
            # If you have a custom endpoint, include base_url= here
            # base_url="https://chatapi.akash.network/api/v1"
        )

        # Call the API and show a spinner while waiting
        with st.spinner("AI is thinking..."):
            try:
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=st.session_state.messages,
                )
                assistant_msg = response.choices[0].message.content
            except Exception as e:
                assistant_msg = f"Error: {e}"

        # Append and display the assistant's reply
        st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
        st.chat_message("assistant").write(assistant_msg)
