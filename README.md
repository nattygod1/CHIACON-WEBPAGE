# CHIACON-WEBPAGE
# Chiacon AI Consultancy – Streamlit Webpage

This is a simple **Streamlit** web app for **Chiacon AI Consultancy**.  
It showcases what Chiacon does in AI and includes a **working AI Email Generator** that creates a personalised outreach email given a company, industry, and role.

---

## How it works

- **Landing content**
  - Headline and description of Chiacon’s AI capabilities.
  - 2–3 example AI use cases (customer support, workflow automation, decision support).
- **AI Email Generator**
  - You enter:
    - Target **company name**
    - **Industry**
    - Recipient **role**
  - The app sends this information to the **Google Gemini API** (via a small Python function) which:
    - Uses a generative model (`gemini-1.5-flash` by default)  
    - Returns a **tailored, professional outreach email** with a subject line.
  - The generated email is displayed in the app so you can copy/paste or adapt it.

If your Gemini API key is not configured, the app will show a helpful warning and a fallback message instead of calling the API.

---

## Tech stack

- **Frontend & backend**: [Streamlit](https://streamlit.io/)
- **Language**: Python
- **AI API**: [Google Gemini](https://ai.google.dev/)

Files:
- `app.py` – main Streamlit app with layout, use-cases, and email generator.
- `requirements.txt` – Python dependencies.

---

## Adding the Chiacon logo

The app will automatically show a logo at the top of the page.

- **Best option (recommended for deployment)**: add a local logo file into an `assets/` folder, for example:
  - `assets/chiacon-logo.png` (preferred)
  - `assets/chiacon-logo.jpg`
  - `assets/chiacon-logo.svg`
  - (or `assets/logo.png` / `assets/logo.svg`)

If no local file exists, the app will try to discover a logo-like image from `chiacon.com` and use that. If that also fails, it falls back to a simple text header.

---

## Running locally

1. **Clone / copy this project** into a folder, then open a terminal in that folder.

2. **Create a virtual environment** (recommended) and activate it, for example:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set your Gemini API key** (you need a Google account and Gemini API key):

   On Windows PowerShell:

   ```bash
   setx GEMINI_API_KEY "your_gemini_api_key_here"
   ```

   Close and reopen your terminal so the environment variable is picked up.

   > Alternatively, in Streamlit you can create a `.streamlit/secrets.toml` file and add:  
   > `GEMINI_API_KEY = "your_gemini_api_key_here"`

5. **Run the Streamlit app**:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL shown in the terminal (usually `http://localhost:8501`) to use the app.

---

## Deploying for a live link (Streamlit Community Cloud)

To make the app accessible via a public URL:

1. **Create a Git repository** in this folder and push it to GitHub (or similar):

   ```bash
   git init
   git add .
   git commit -m "Initial Chiacon AI web app"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```

2. Go to **Streamlit Community Cloud** (Streamlit Cloud) in your browser and sign in.

3. Click **“New app”**, connect your GitHub account, and select the repository and branch.

4. Set the **main file** to `app.py`.

5. Under **Advanced settings / Secrets**, add your Gemini key, for example:

   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```

6. Click **Deploy** – Streamlit will build the app using `requirements.txt` and give you a **public URL** that you can share as your live Chiacon AI webpage.

Once deployed, any visitor can open the live link, read about Chiacon’s AI capabilities, see example use cases, and generate personalised outreach emails via the integrated AI feature.
