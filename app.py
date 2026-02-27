import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

import google.generativeai as genai
import streamlit as st


st.set_page_config(
    page_title="Chiacon AI Consultancy",
    layout="wide",
)


def inject_styles() -> None:
    st.markdown(
        """
<style>
  /* App background */
  [data-testid="stAppViewContainer"]{
    background: linear-gradient(135deg, #f6f9ff 0%, #f5f3ff 40%, #ffffff 100%);
  }
  [data-testid="stAppViewContainer"]::before{
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background:
      radial-gradient(600px 400px at 12% 18%, rgba(79, 70, 229, 0.18), transparent 60%),
      radial-gradient(520px 360px at 85% 22%, rgba(6, 182, 212, 0.16), transparent 62%),
      radial-gradient(620px 420px at 58% 88%, rgba(236, 72, 153, 0.12), transparent 64%);
    filter: saturate(115%);
  }
  [data-testid="stHeader"]{
    background: rgba(0,0,0,0);
  }
  [data-testid="stAppViewContainer"] > .main{
    position: relative;
    z-index: 1;
  }

  /* Layout polish */
  .main .block-container{
    padding-top: 3.25rem;
    padding-bottom: 3.25rem;
    max-width: 1120px;
  }

  /* Typography */
  h1, h2, h3{
    letter-spacing: -0.02em;
  }
  h1{
    font-weight: 850;
    line-height: 1.06;
  }
  h2{
    font-weight: 780;
  }
  /* Brand row */
  .brand-row{
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 0.25rem;
  }
  .brand-row .brand-name{
    font-size: 0.98rem;
    font-weight: 700;
    color: rgba(15, 23, 42, 0.80);
    letter-spacing: 0.02em;
    text-transform: uppercase;
  }

  /* Primary button */
  .stButton > button{
    border: none;
    border-radius: 14px;
    padding: 0.65rem 1.05rem;
    background: linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%);
    color: white;
    box-shadow: 0 10px 25px rgba(79, 70, 229, 0.18);
  }
  .stButton > button:hover{
    transform: translateY(-1px);
    box-shadow: 0 14px 30px rgba(79, 70, 229, 0.22);
  }
  .stButton > button:active{
    transform: translateY(0px);
  }

  /* Inputs */
  .stTextInput input{
    border-radius: 12px !important;
  }

  /* Metrics look like cards */
  div[data-testid="stMetric"]{
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(15, 23, 42, 0.08);
    border-radius: 16px;
    padding: 14px 16px;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
    backdrop-filter: blur(8px);
  }

  /* Code output (generated email) */
  .stCodeBlock{
    border-radius: 16px;
    border: 1px solid rgba(15, 23, 42, 0.10);
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
  }
</style>
""",
        unsafe_allow_html=True,
    )


def _local_logo_path() -> Path | None:
    candidates = [
        Path("assets/chiacon-logo.png"),
        Path("assets/chiacon-logo.jpg"),
        Path("assets/chiacon-logo.jpeg"),
        Path("assets/chiacon-logo.webp"),
        Path("assets/chiacon-logo.svg"),
        Path("assets/logo.png"),
        Path("assets/logo.jpg"),
        Path("assets/logo.svg"),
    ]
    for p in candidates:
        if p.exists() and p.is_file():
            return p
    return None


@st.cache_data(ttl=60 * 60 * 24)
def _discover_logo_from_website() -> str | None:
    """
    Best-effort: discover a logo-like asset from chiacon.com (Wix static media).
    Falls back to None if discovery fails.
    """
    pages = [
        "https://www.chiacon.com/",
        "https://www.chiacon.com/aboutus",
    ]
    for page in pages:
        try:
            html = (
                urllib.request.urlopen(page, timeout=20)
                .read()
                .decode("utf-8", errors="ignore")
            )
        except Exception:
            continue

        media_urls = set(
            re.findall(
                r"https?://static\.wixstatic\.com/media/[^\"]+?\.(?:png|jpg|jpeg|webp|svg)",
                html,
                flags=re.IGNORECASE,
            )
        )
        if not media_urls:
            continue

        preferred = sorted(
            [u for u in media_urls if re.search(r"logo|chiacon|chia", u, re.I)],
            key=len,
        )
        if preferred:
            return preferred[0]
    return None


def render_logo(width: int = 140) -> None:
    """
    Render Chiacon logo:
    - Prefer a local logo in ./assets/
    - Else attempt discovery from chiacon.com
    - Else show a simple text fallback
    """
    local = _local_logo_path()
    if local is not None:
        if local.suffix.lower() == ".svg":
            svg = local.read_text(encoding="utf-8", errors="ignore")
            st.markdown(
                f"<div class='brand-row'><img alt='Chiacon' width='{width}' src='data:image/svg+xml;utf8,{urllib.parse.quote(svg)}' /></div>",
                unsafe_allow_html=True,
            )
        else:
            st.image(str(local), width=width)
        return

    remote = _discover_logo_from_website()
    if remote:
        st.image(remote, width=width)
        return

    st.markdown(
        "<div class='brand-row'><div class='brand-name'>Chiacon</div></div>",
        unsafe_allow_html=True,
    )


@st.cache_resource
def get_gemini_model() -> genai.GenerativeModel | None:
    """
    Create and cache a Gemini model if an API key is available.
    Returns None if no key is configured so the UI can show a helpful message.
    """
    api_key: str | None = None
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")  # type: ignore[attr-defined]
    except Exception:
        api_key = None

    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def generate_outreach_email(company: str, industry: str, role: str) -> str:
    """
    Call the Gemini API to generate a personalized outreach email.
    """
    model = get_gemini_model()
    if model is None:
        return (
            "GEMINI_API_KEY is not set.\n\n"
            "Please configure your Gemini API key as either:\n"
            "- an environment variable named GEMINI_API_KEY (or GOOGLE_API_KEY), or\n"
            "- a Streamlit secret named GEMINI_API_KEY"
        )

    prompt = f"""
You are an expert B2B sales copywriter helping an AI consultancy called Chiacon.

Write a concise, friendly cold outreach email to a potential client.

Details:
- Consultancy: Chiacon (AI strategy and implementation)
- Target company: {company or "a prospective client"}
- Industry: {industry or "N/A"}
- Recipient role: {role or "N/A"}

Goals for the email:
- Be professional but approachable.
- Clearly explain how AI can create value for this specific industry and role.
- Reference that Chiacon can help with strategy, prototyping, and productionizing AI solutions.
- Keep it to 3–5 paragraphs, plus a short subject line.

Output format:
Subject: <subject line>

<email body>
"""

    try:
        response = model.generate_content(prompt)
        text = getattr(response, "text", None)
        if not text:
            return "The AI model did not return any text. Please try again."
        return text.strip()
    except Exception as e:  # noqa: BLE001
        message = str(e)
        if "429" in message or "insufficient_quota" in message:
            return (
                "The Gemini API reported that your quota is exhausted or rate limited.\n"
                "Please check your Google AI Studio / billing limits and try again."
            )
        return f"Error while generating email: {message}"


def render_hero_section() -> None:
    brand_left, brand_right = st.columns([1, 6], vertical_alignment="center")
    with brand_left:
        render_logo(width=140)
    with brand_right:
        st.title("Unlock Practical AI with Chiacon")
    st.subheader("From idea to impact: strategy, prototypes, and production-grade AI solutions.")

    left, right = st.columns([2, 1])
    with left:
        st.markdown(
            """
Chiacon is a leading AI consultancy helping organisations **turn AI buzzwords into real business outcomes**.

We partner with teams to:
- Identify the highest-value AI opportunities
- Rapidly prototype solutions
- Safely deploy AI into production workflows
"""
        )

    with right:
        st.markdown("### AI capabilities at a glance")
        st.metric(label="Time to first prototype", value="2–4 weeks")
        st.metric(label="Focus", value="Applied AI & automation")
        st.metric(label="Engagement model", value="Advisory & delivery")


def render_use_cases() -> None:
    st.markdown("### Example AI use cases we deliver")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
**Intelligent customer support**
- AI copilots for support teams  
- Ticket summarisation and routing  
- Knowledge-base chatbots connected to your docs
"""
        )

    with col2:
        st.markdown(
            """
**Workflow automation**
- Document understanding and data extraction  
- Automating repetitive back-office processes  
- Human-in-the-loop review pipelines
"""
        )

    with col3:
        st.markdown(
            """
**Decision support & analytics**
- Natural-language querying over company data  
- Scenario simulations powered by AI  
- Executive dashboards with AI insights
"""
        )


def render_email_generator() -> None:
    st.markdown("---")
    st.header("AI Email Generator")
    st.caption(
        "Generate a tailored outreach email you could send to a potential client, powered by Google Gemini."
    )

    model_available = get_gemini_model() is not None
    if not model_available:
        st.warning(
            "To enable the AI Email Generator, set your `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) "
            "environment variable or configure it via `st.secrets['GEMINI_API_KEY']`, then restart the app."
        )

    with st.form("email_form"):
        company = st.text_input("Target company name", placeholder="Acme Corp")
        industry = st.text_input("Industry", placeholder="Fintech, Manufacturing, Retail, etc.")
        role = st.text_input("Recipient role", placeholder="Head of Operations, CTO, etc.")

        submitted = st.form_submit_button("Generate outreach email", type="primary")

    if submitted:
        if not company and not industry and not role:
            st.error("Please provide at least one detail (company, industry, or role).")
            return

        with st.spinner("Asking the AI to craft your email..."):
            email_text = generate_outreach_email(company, industry, role)

        st.markdown("#### Generated email")
        st.code(email_text, language="markdown")


def main() -> None:
    inject_styles()
    render_hero_section()
    render_use_cases()
    render_email_generator()


if __name__ == "__main__":
    main()

