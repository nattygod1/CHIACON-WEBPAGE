# CHIACON-WEBPAGE
# Chiacon AI Consultancy – Streamlit Webpage

# Chiacon – AI Webpage (Streamlit)

This project is a small, polished Streamlit website for **Chiacon**. It introduces Chiacon’s AI capabilities, gives a few practical use cases, and includes a working **AI Email Generator** to create personalised outreach emails.

---

## How it works

When you open the app, you’ll see:

- **A simple Chiacon landing page**
  - A headline focused on practical AI outcomes
  - A short description of what Chiacon does
  - 2–3 example AI use cases (support, automation, decision support)

- **AI Email Generator (Gemini-powered)**
  - You enter a **company name**, **industry**, and **role**
  - The app sends those details to **Google Gemini**
  - Gemini returns a ready-to-use outreach email with a **subject line** and a short, professional body
  - The email is shown on the page so you can copy, edit, and send

To generate emails, the app needs a valid **Gemini API key** available as `GEMINI_API_KEY` (via Streamlit secrets or environment variables). If the key isn’t set, the app will show a clear warning instead of calling the API.



## Tech stack

- **Frontend + backend**: [Streamlit](https://streamlit.io/)
- **Language**: Python
- **AI model/API**: [Google Gemini](https://ai.google.dev/) (via `google-generativeai`)

---

## Project files

- `app.py` — Streamlit UI + Gemini email generator
- `requirements.txt` — dependencies


