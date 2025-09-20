from config import model

def call_gemini(prompt: str, max_output_chars: int = 15000) -> str:
    response = model.generate_content(
        contents=prompt,
        generation_config={"temperature": 0.15, "top_p": 0.9},
    )
    out = response.text.strip()
    return out[:max_output_chars]
