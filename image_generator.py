import streamlit as st
import openai

# Image Generator Instructions (system prompt)
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
- nologo (optional): Set to true to disable the logo rendering. Please always set nologo to true unless specified.

## Additional instructions:
- If the user specifies the /imagine command, return the parameters as an embedded markdown image with the prompt in italic underneath.

## Example:
![{description}](https://image.pollinations.ai/prompt/{description}?width={width}&height={height})
*{description}*
"""

def run():
    st.title("🤖 AI Image Generator")
    st.caption("Chat with an AI assistant to generate creative images.")

    # Initialize state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": PREPROMPT},
            {"role": "assistant", "content": "Hi there! Tell me what image you'd like to create."}
        ]

    # Clear chat
    if st.button("🗑️ Clear Chat", key="clear"):
        st.session_state.messages = [
            {"role": "system", "content": PREPROMPT},
            {"role": "assistant", "content": "Hi there! Tell me what image you'd like to create."}
        ]

    # Display conversation
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # ---- User Input ----
    prompt = st.chat_input("Type your image prompt...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Advanced options hidden in expander
        with st.expander("Advanced Settings (optional)"):
            # Model selection
            model = st.radio(
                "Choose model:",
                ["flux", "flux-realism", "any-dark", "flux-anime", "flux-3d", "turbo"],
                index=0
            )

            # Aspect ratio presets
            aspect = st.radio(
                "Image size:",
                ["Square (1024x1024)", "Portrait (768x1024)", "Landscape (1024x768)"],
                index=0
            )
            size_map = {
                "Square (1024x1024)": (1024, 1024),
                "Portrait (768x1024)": (768, 1024),
                "Landscape (1024x768)": (1024, 768)
            }
            width, height = size_map[aspect]

            # Seed
            use_seed = st.checkbox("Specify seed (for reproducible results)")
            if use_seed:
                seed = st.number_input("Seed value:", min_value=0, max_value=2**32-1, value=0)
            else:
                seed = None

            # Disable logo
            nologo = st.checkbox("Disable logo on output", value=True)

        # Call OpenAI API
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        with st.spinner("Generating image parameters..."):
            messages = st.session_state.messages + [{"role": "assistant", "content": prompt}]
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                )
                assistant_msg = response.choices[0].message.content
            except Exception as e:
                assistant_msg = f"Error: {e}"

        # Append and display assistant response
        st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
        st.chat_message("assistant").write(assistant_msg)
