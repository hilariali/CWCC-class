# AI Tool Hub

This repository contains several Streamlit tools with **passkey authentication** to restrict access to authorized users only.

## Features

- **🔐 Passkey Authentication** – Access is restricted to users with the correct passkey
- **YouTube Quiz Generator** – Paste a video URL to create a quiz from its transcript.
- **AI Chatbot** – Chat with an AI assistant using your API key.
- **File Chat Tool** – Upload documents and ask questions about them.
- **Website Summarizer** – Provide a URL to get a summary and chat about that webpage.
- **Image Generator** – Create images from text prompts.
- **Text to Speech** – Convert text into spoken audio using Pollinations API.

## Setup

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Streamlit settings**
   - Create `.streamlit/config.toml` with:
     ```toml
     [server]
     fileWatcherType = "none"
     ```
4. **Set up authentication (Important!)**
   - For local development: Create `.streamlit/secrets.toml` with:
     ```toml
     [general]
     PASSKEY = "2025"
     ```
   - For Streamlit Cloud deployment: Add `PASSKEY = "2025"` to your Streamlit Cloud secrets
   - **Note**: The `.streamlit/secrets.toml` file is included in `.gitignore` for security
5. **Set OpenAI secrets**
   - In Streamlit Cloud secrets or local secrets file, add:
     - `OPENAI_API_KEY`
     - `OPENAI_BASE_URL`
6. **Deploy or run locally**
   ```bash
   streamlit run streamlit_app.py
   ```

## Authentication

The application now requires a passkey for access:
- Default passkey: `2025`
- Users must enter the correct passkey to access any functionality
- Authentication state persists during the session
- Users can logout using the logout button in the sidebar
- Invalid passkey attempts show clear error messages

### Security Notes
- The passkey is stored securely in Streamlit secrets
- Authentication state is managed using Streamlit's session state
- The secrets file is excluded from version control via `.gitignore`
