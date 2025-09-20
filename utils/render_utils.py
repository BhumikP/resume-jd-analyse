from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def render_markdown_like_to_pdf(md_text: str) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin_x, y, line_height = 50, height - 50, 16

    def draw_line(text, bold=False, indent=0):
        nonlocal y
        if y < 50:
            c.showPage()
            y = height - 50
        c.setFont("Helvetica-Bold" if bold else "Helvetica", 10 if not bold else 11)
        c.drawString(margin_x + indent, y, text)
        y -= line_height

    for raw_line in md_text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            y -= 6
            continue
        if line.startswith("## "):
            draw_line(line[3:].strip(), bold=True)
        elif line.startswith("- "):
            draw_line("• " + line[2:].strip(), indent=12)
        elif line.startswith("[IMPROVE]"):
            draw_line(line.strip(), indent=12)
        else:
            max_chars = 95
            while len(line) > max_chars:
                draw_line(line[:max_chars])
                line = line[max_chars:]
            if line:
                draw_line(line)
    c.save()
    buffer.seek(0)
    return buffer
