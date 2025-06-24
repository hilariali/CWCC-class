import streamlit as st
import openai

# Image Generator Instructions
PREPROMPT = """
# Image Generator Instructions

You are an image generator. The user provides a prompt. Please infer the following parameters for image generation:

- **Prompt:** [prompt, max 50 words]
- **Seed:** [seed]
- **Width:** [width]
- **Height:** [height]
- **Model:** [model]

## Key points:
- If the user's prompt is short, add creative details to make it about 50 words suitable for an image generator AI.
- Each seed value creates a unique image for a given prompt.
- To create variations of an image without changing its content:
  - Keep the prompt the same and change only the seed.
- To alter the content of an image:
  - Modify the prompt and keep the seed unchanged.
- Infer width and height around 1024x1024 or other aspect ratios if it makes sense.
- Infer the most appropriate model name based on the content and style described in the prompt.

## Default params:
- prompt (required): The text description of the image you want to generate.
- model (optional): The model to use for generation. Options: 'flux', 'flux-realism', 'any-dark', 'flux-anime', 'flux-3d', 'turbo' (default: 'flux')
  - Infer the most suitable model based on the prompt's content and style.
- seed (optional): Seed for reproducible results (default: random).
- width/height (optional): Default 1024x1024.
- nologo (optional): Set to true to disable the logo rendering.

## Additional instructions:
- If the user specifies the /imagine command, return the parameters as an embedded markdown image with the prompt in italic underneath.

## Example:
![{description}](https://image.pollinations.ai/prompt/{description}?width={width}&height={height})
*{description}*
""""

def run():
    st.title("🤖 AI Chatbot")
    st.caption("🚀 Chat with an AI assistant powered by your secret API key.")

    # Initialize conversation with system preprompt
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": PREPROMPT},
            {"role": "assistant", "content": "Hi there! How can I help you today?"}
        ]

    # Clear Chat button resets to preprompt and greeting
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {"role": "system", "content": PREPROMPT},
            {"role": "assistant", "content": "Hi there! How can I help you today?"}
        ]

    # Model selection
    model_options = [
        "DeepSeek-R1-0528",
        "Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
        "Qwen3-235B-A22B-FP8",
    ]
    selected_model = st.selectbox("Choose a model:", model_options)

    # Display conversation
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Handle new user input
    prompt = st.chat_input("Type your message...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        with st.spinner("AI is thinking..."):
            try:
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=st.session_state.messages,
                )
                assistant_msg = response.choices[0].message.content
            except Exception as e:
                assistant_msg = f"Error: {e}"

        st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
        st.chat_message("assistant").write(assistant_msg)
