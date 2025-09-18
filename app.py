import streamlit as st
import os
import fitz  # PyMuPDF
import google.generativeai as genai

# -----------------------------
# Setup Gemini API
# -----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------------
# Helper: Extract text from PDF
# -----------------------------
def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
    except Exception as e:
        st.error(f"❌ Error extracting text from PDF: {e}")
    return text.strip()

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Resume JD Matcher", layout="centered")

st.title("📄 AI Resume – JD Matcher")
st.write("Upload your resume PDF and paste the Job Description. Get **crystal-clear improvements** to match the role.")

# Upload PDF Resume
uploaded_resume = st.file_uploader("📎 Upload Resume (PDF)", type=["pdf"])

resume_text = ""
if uploaded_resume is not None:
    resume_text = extract_text_from_pdf(uploaded_resume)

# Job description text area
jd = st.text_area("📝 Paste the Job Description (JD):", height=200, placeholder="Copy-paste the job description here...")

if st.button("🔍 Analyze Resume vs JD"):
    if not resume_text or not jd.strip():
        st.warning("⚠️ Please provide both a valid resume PDF and JD.")
    else:
        with st.spinner("Analyzing resume..."):
            prompt = f"""
You are an expert resume coach. Compare the following **Resume** and **Job Description (JD)**.
Return **only a crystal-clear improvement checklist** with points that the candidate must add or improve in the resume 
to qualify for the job. 

Strict rules:
- Use **bold** for key skills/points.
- No vague suggestions like "maybe add" or "could improve".
- No multiple-choice answers, just **direct actionable points**.
- Keep it short, precise, and professional.

Resume:
{resume_text}

Job Description:
{jd}
"""

            response = model.generate_content(prompt)
            result = response.text.strip()

        st.subheader("✅ Improvement Checklist")
        st.markdown(result)
