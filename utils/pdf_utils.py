import fitz  # PyMuPDF

def extract_structured_text_from_pdf(uploaded_file):
    blocks = []
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for pno, page in enumerate(doc):
            page_dict = page.get_text("dict")
            for block in page_dict.get("blocks", []):
                block_text = ""
                sizes = []
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        txt = span.get("text", "")
                        size = span.get("size", 0)
                        sizes.append(size)
                        block_text += txt
                    block_text += "\n"
                block_text = block_text.strip()
                if not block_text:
                    continue
                avg_size = (sum(sizes) / len(sizes)) if sizes else 0
                is_heading = avg_size >= 12 or (len(block_text) <= 60 and block_text.isupper())
                blocks.append({"text": block_text, "is_heading": bool(is_heading), "page": pno})
    except Exception as e:
        raise RuntimeError(f"PDF extraction error: {e}")
    return {"blocks": blocks}

def blocks_to_plain_resume_text(blocks_struct):
    blocks = blocks_struct.get("blocks", [])
    out_lines = []
    for b in blocks:
        if b["is_heading"]:
            out_lines.append(f"## {b['text']}")
        else:
            out_lines.extend([line.strip() for line in b["text"].splitlines() if line.strip()])
    return "\n".join(out_lines)

def insert_bullets_into_pdf(original_pdf_stream, added_bullets_by_section):
    """
    Insert new bullets into the appropriate sections of the original PDF, matching the style and preserving formatting.
    Args:
        original_pdf_stream: The uploaded PDF file stream (BytesIO or similar).
        added_bullets_by_section: Dict mapping section names (e.g., 'Skills') to list of new bullet strings.
    Returns:
        BytesIO buffer of the modified PDF.
    """
    import fitz
    from io import BytesIO
    import sys

    # Read the original PDF
    original_pdf_stream.seek(0)
    doc = fitz.open(stream=original_pdf_stream.read(), filetype="pdf")

    # Find section headings and their locations
    section_locs = {}
    for page_num, page in enumerate(doc):
        blocks = page.get_text("blocks")
        for b in blocks:
            text = b[4].strip()
            if not text:
                continue
            # Heuristic: section headings are often all-caps or match known section names
            if text.isupper() or text.lower() in [s.lower() for s in added_bullets_by_section.keys()]:
                section_locs[text.lower()] = (page_num, b)
    print(f"[DEBUG] Section locations found: {section_locs}", file=sys.stderr)
    print(f"[DEBUG] Bullets to insert: {added_bullets_by_section}", file=sys.stderr)

    # Insert new bullets in the right section
    for section, bullets in added_bullets_by_section.items():
        section_key = section.lower()
        if section_key in section_locs:
            page_num, block = section_locs[section_key]
            page = doc[page_num]
            # Insert bullets just below the section heading
            x0, y0, x1, y1, text, block_no = block
            insert_y = y1 + 2  # a little below the heading
            for bullet in bullets:
                print(f"[DEBUG] Inserting bullet '{bullet}' in section '{section}' on page {page_num}", file=sys.stderr)
                # Try to match the style: indent, font, etc.
                page.insert_text((x0 + 20, insert_y), f"• {bullet}", fontsize=11, fontname="helv")
                insert_y += 14  # space between bullets
        else:
            # If section not found, add to the end of the first page
            page = doc[0]
            insert_y = 60 + 14 * len(page.get_text("text").splitlines())
            for bullet in bullets:
                print(f"[DEBUG] Inserting bullet '{bullet}' at end of first page (section '{section}' not found)", file=sys.stderr)
                page.insert_text((60, insert_y), f"• {bullet}", fontsize=11, fontname="helv")
                insert_y += 14

    # Save to buffer
    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf
