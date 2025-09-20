def generate_version_prompts(original_resume_text, jd_text):
    base = (
        "You are a professional resume writer. Return the improved resume text in plain text:\n"
        "- '## ' for section headings\n"
        "- '- ' for bullets\n"
        "- Preserve original structure\n"
        "- Do NOT invent facts\n"
        "- Prefix added bullets with '[ADDED_FROM_JD] '\n"
    )

    prompts = {
        "A": (
            "You are a professional resume writer. Your task is to improve the provided resume by matching it to the job description (JD).\n"
            "Instructions:\n"
            "- Analyze the structure and sections of the original resume (e.g., Skills, Experience, Projects, Education).\n"
            "- For each missing skill, qualification, or relevant point from the JD, add a new bullet in the most appropriate section, matching the section's style and bullet format.\n"
            "- Preserve the original order, formatting, and do NOT invent facts.\n"
            "- Prefix each bullet you add with '[ADDED_FROM_JD]' for identification.\n"
            "- Output the improved resume in plain text, using:\n"
            "    - '## ' for section headings\n"
            "    - '- ' for bullets\n"
            "    - The same section and bullet order as the original resume\n"
            f"Resume:\n{original_resume_text}\n\nJD:\n{jd_text}\n"
        ),
        "B": (
            "You are a professional resume writer and ATS optimization expert. Your task is to improve the provided resume by matching it to the job description (JD) and optimizing for ATS systems.\n"
            "Instructions:\n"
            "- Carefully analyze the structure and sections of the original resume (e.g., Skills, Experience, Projects, Education).\n"
            "- For each new point or bullet you add from the JD, insert it into the most appropriate section, matching the section's style, indentation, and bullet format.\n"
            "- Use action verbs, relevant keywords from the JD, and keep each bullet concise (ideally ≤2 lines).\n"
            "- Preserve the original order and formatting of all sections and bullets.\n"
            "- Do NOT invent facts or add information not present in the resume or JD.\n"
            "- Prefix each bullet you add with '[ADDED_FROM_JD]' for identification.\n"
            "- Output the improved resume in plain text, using:\n"
            "    - '## ' for section headings\n"
            "    - '- ' for bullets\n"
            "    - The same section and bullet order as the original resume\n"
            "- Example output:\n"
            "    ## Skills\n"
            "    - Python\n"
            "    - [ADDED_FROM_JD] Data Analysis\n"
            "    ## Experience\n"
            "    - Software Engineer at XYZ\n"
            "    - [ADDED_FROM_JD] Led migration to cloud infrastructure\n"
            f"Resume:\n{original_resume_text}\n\nJD:\n{jd_text}\n"
        ),
        "C": (
            "You are a professional resume writer and ATS expert. Your task is to review the provided resume against the job description (JD) and annotate it for improvement.\n"
            "Instructions:\n"
            "- Analyze the structure and sections of the original resume (e.g., Skills, Experience, Projects, Education).\n"
            "- For each section, if you find missing skills, keywords, or ATS-relevant information from the JD, add a bullet with '[IMPROVE]' at the start, describing what should be added or improved.\n"
            "- Do NOT invent facts or add information not present in the resume or JD.\n"
            "- Output the annotated resume in plain text, using:\n"
            "    - '## ' for section headings\n"
            "    - '- ' for bullets\n"
            "    - The same section and bullet order as the original resume\n"
            "- Example output:\n"
            "    ## Skills\n"
            "    - Python\n"
            "    - [IMPROVE] Add 'Data Analysis' if you have experience\n"
            "    ## Experience\n"
            "    - Software Engineer at XYZ\n"
            "    - [IMPROVE] Add a bullet about cloud migration if applicable\n"
            f"Resume:\n{original_resume_text}\n\nJD:\n{jd_text}\n"
        ),
    }
    return prompts
