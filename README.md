# AI Tool Hub

This repository contains several Streamlit tools:

- **YouTube Quiz Generator** – Paste a video URL to create a quiz from its transcript.
- **AI Chatbot** – Chat with an AI assistant using your API key.
- **File Chat Tool** – Upload documents and ask questions about them.
- **Website Summarizer** – Provide a URL to get a summary and chat about that webpage.

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
4. **Set OpenAI secrets**
   - In Streamlit Cloud secrets, add:
     - `OPENAI_API_KEY`
     - `OPENAI_BASE_URL`
5. **Deploy or run locally**
   ```bash
   streamlit run streamlit_app.py
   ```
