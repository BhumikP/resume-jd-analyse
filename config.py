import os
import google.generativeai as genai

# API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY environment variable.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Model
REWRITE_MODEL = "gemini-1.5-flash"
model = genai.GenerativeModel(REWRITE_MODEL)
