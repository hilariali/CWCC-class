# dummy_tool1.py

import streamlit as st
import openai

def run():
    st.header("🤖 AI Chatbot (Dummy Tool 1)")
    st.write("Chat with an AI assistant powered by your OpenAI API key.")

    # ----------------------------------------------------------------------------
    # 1) Initialize the new OpenAI client (v1.0.0+)
    # ----------------------------------------------------------------------------
    if "client" not in st.session_state:
        st.session_state.client = openai.OpenAI(
            api_key=st.secrets["OPENAI_API_KEY"]
            # If you use a custom endpoint, uncomment & adjust below:
            # base_url="https://chatapi.akash.network/api/v1"
        )

    # ----------------------------------------------------------------------------
    # 2) Initialize or retrieve conversation history
    # ----------------------------------------------------------------------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    # ----------------------------------------------------------------------------
    # 3) Model selection (always at the top)
    # ----------------------------------------------------------------------------
    model_options = [
        "DeepSeek-R1-0528",
        "Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
        "Qwen3-235B-A22B-FP8",
    ]
    selected_model = st.selectbox("Choose a model:", model_options)

    # ----------------------------------------------------------------------------
    # 4) Display conversation inside a scrollable container
    # ----------------------------------------------------------------------------
    st.markdown("---")
    # Build HTML for all messages (excluding system prompt)
    messages_html = ""
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            messages_html += f"<p style='margin:4px 0;'><strong>You:</strong> {msg['content']}</p>"
        elif msg["role"] == "assistant":
            messages_html += f"<p style='margin:4px 0;'><strong>AI:</strong> {msg['content']}</p>"

    scrollable_div = f"""
        <div style="
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 8px;
            background-color: #fafafa;
        ">
            {messages_html}
        </div>
    """

    st.markdown(scrollable_div, unsafe_allow_html=True)
    st.markdown("---")

    # ----------------------------------------------------------------------------
    # 5) Chat input form (at the bottom)
    # ----------------------------------------------------------------------------
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Your message:",
            key="input_text",
            height=100,
            placeholder="Type your message here..."
        )
        submitted = st.form_submit_button("Send")
        if submitted:
            stripped = user_input.strip()
            if stripped:
                # Append user's message
                st.session_state.chat_history.append(
                    {"role": "user", "content": stripped}
                )

                # Call the OpenAI API with a spinner
                with st.spinner("AI is thinking..."):
                    try:
                        response = st.session_state.client.chat.completions.create(
                            model=selected_model,
                            messages=st.session_state.chat_history,
                        )
                        assistant_msg = response.choices[0].message.content
                    except Exception as e:
                        assistant_msg = f"Error: {e}"

                # Append assistant's reply
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": assistant_msg}
                )
            else:
                st.warning("Please enter a message before sending.")
