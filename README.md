# TRUVIA — Multi-Agent Digital Trust & Safety

Evidence-first Streamlit application using CrewAI and Groq. It provides AI-assisted triage of user-supplied suspicious messages and URL strings, plus pasted OCR/QR/audio-transcript text.

## Features
- Six specialized CrewAI agents: intake, social engineering, URL structure, evidence verification, risk triage, and report writing.
- Groq-hosted Llama model through CrewAI's LLM integration.
- Dark responsive Streamlit workspace, sidebar settings, analysis form, agent task summary, Markdown report download.
- Input length validation and explicit uncertainty / no-live-check warnings.
- No automatic blocking, reporting, or third-party contact.

## Setup
Python 3.11 recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your Groq key to .env
streamlit run app.py
```

Get a Groq API key from https://console.groq.com/ and keep it private. For Streamlit Community Cloud, add `GROQ_API_KEY` in app Secrets.

## Important limitations
This MVP analyzes only content the user provides. It does not perform live URL browsing, DNS/TLS checks, malware scanning, OCR, QR decoding, or speech-to-text. Paste OCR text, decoded QR content, or an audio transcript. The model can still make mistakes; verify important claims through independently obtained official channels.

## Six-person team plan
1. UI/UX and Streamlit
2. CrewAI workflow and orchestration
3. Input/evidence processing
4. Groq integration and prompt quality
5. Verification, evaluation and test cases
6. Deployment, documentation and pitch

## Project structure
```
app.py
truvia/
  agents.py
  evidence.py
  workflow.py
requirements.txt
.env.example
```
