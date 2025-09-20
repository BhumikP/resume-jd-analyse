import streamlit as st
from utils.pdf_utils import extract_structured_text_from_pdf, blocks_to_plain_resume_text, insert_bullets_into_pdf
from utils.render_utils import render_markdown_like_to_pdf
from utils.prompts import generate_version_prompts
from utils.gemini_utils import call_gemini
from utils.parse_utils import parse_added_bullets_from_generated, remove_or_replace_added_bullets
import io

st.set_page_config(page_title="Resume AI", layout="wide")
st.title("AI Resume Generator with JD Matching & ATS Versions")

uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description", height=220)

# Wrap uploaded_resume in BytesIO for re-use
if uploaded_resume is not None:
    uploaded_pdf_bytes = uploaded_resume.read()
    uploaded_pdf_io = io.BytesIO(uploaded_pdf_bytes)
else:
    uploaded_pdf_io = None

if st.button("Generate Versions"):
    if not uploaded_pdf_io or not jd_text.strip():
        st.warning("Upload resume and paste JD first.")
    else:
        blocks_struct = extract_structured_text_from_pdf(io.BytesIO(uploaded_pdf_bytes))
        resume_text = blocks_to_plain_resume_text(blocks_struct)
        prompts = generate_version_prompts(resume_text, jd_text)

        st.session_state.generated = {}
        st.session_state.added_info = {}
        for key, prompt in prompts.items():
            out = call_gemini(prompt)
            st.session_state.generated[key] = out
            st.session_state.added_info[key] = parse_added_bullets_from_generated(out)
        st.success("Generated all versions.")

if "generated" in st.session_state:
    for key, text in st.session_state.generated.items():
        st.subheader(f"Version {key}")
        st.text_area(f"Preview {key}", value=text, height=200, key=f"gen_{key}")
        added_list = st.session_state.added_info[key]

        if added_list:
            edits_map = {}
            for item in added_list:
                with st.expander(item["bullet_text"], expanded=False):
                    keep = st.checkbox("Keep bullet?", True, key=f"{key}_{item['id']}_keep")
                    edit = st.text_area("Edit text:", item["bullet_text"], key=f"{key}_{item['id']}_edit")
                    edits_map[item["id"]] = {"keep": keep, "text": edit}
            if st.button(f"Finalize {key}"):
                final_text = remove_or_replace_added_bullets(text, edits_map)
                if key == "B":
                    added_bullets_by_section = {}
                    for item in added_list:
                        if edits_map.get(item["id"], {"keep": True})["keep"]:
                            bullet = edits_map[item["id"]]["text"] or item["bullet_text"]
                            bullet_lower = bullet.lower()
                            if any(word in bullet_lower for word in ["skill", "proficient", "expertise"]):
                                section = "Skills"
                            elif any(word in bullet_lower for word in ["project", "developed", "built"]):
                                section = "Projects"
                            elif any(word in bullet_lower for word in ["experience", "worked", "responsible", "managed", "engineer", "analyst", "developer"]):
                                section = "Experience"
                            else:
                                section = "Other"
                            added_bullets_by_section.setdefault(section, []).append(bullet)
                    st.write("[DEBUG] Bullets to insert:", added_bullets_by_section)
                    if not added_bullets_by_section:
                        st.info("No new bullets to insert into the PDF for Version B.")
                        pdf_buf = io.BytesIO(uploaded_pdf_bytes)
                    else:
                        # Also show section_locs from the PDF for debugging
                        import fitz
                        uploaded_pdf_io_debug = io.BytesIO(uploaded_pdf_bytes)
                        doc_debug = fitz.open(stream=uploaded_pdf_io_debug.read(), filetype="pdf")
                        section_locs_debug = {}
                        for page_num, page in enumerate(doc_debug):
                            blocks = page.get_text("blocks")
                            for b in blocks:
                                text = b[4].strip()
                                if not text:
                                    continue
                                if text.isupper() or text.lower() in [s.lower() for s in added_bullets_by_section.keys()]:
                                    section_locs_debug[text.lower()] = (page_num, b)
                        st.write("[DEBUG] Section locations found:", section_locs_debug)
                        pdf_buf = insert_bullets_into_pdf(io.BytesIO(uploaded_pdf_bytes), added_bullets_by_section)
                else:
                    pdf_buf = render_markdown_like_to_pdf(final_text)
                st.download_button(
                    f"⬇️ Download Version {key}",
                    pdf_buf,
                    file_name=f"resume_{key}.pdf",
                    mime="application/pdf"
                )
        else:
            st.info("No JD-derived bullets found.")
