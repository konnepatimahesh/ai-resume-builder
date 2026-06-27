from fpdf import FPDF
import os
import re

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts")

# Characters DejaVu Sans renders reliably in fpdf2's simple (non-shaping) layout engine.
_SAFE_RANGES = [
    (0x0009, 0x000A),
    (0x0020, 0x007E),
    (0x00A0, 0x024F),
    (0x0370, 0x03FF),
    (0x0400, 0x04FF),
    (0x2010, 0x2027),
]


def _is_safe_char(ch):
    cp = ord(ch)
    return any(start <= cp <= end for start, end in _SAFE_RANGES)


def _clean_char(ch):
    return ch if _is_safe_char(ch) else "?"


def _sanitize(text):
    cleaned = "".join(_clean_char(ch) for ch in text)
    return re.sub(r'\?{2,}', '?', cleaned)


def generate_pdf(optimized_text, output_path):
    pdf = FPDF()
    pdf.set_margins(left=15, top=15, right=15)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_font("DejaVu", "",  os.path.join(FONT_DIR, "DejaVuSans.ttf"),      uni=True)
    pdf.add_font("DejaVu", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), uni=True)
    pdf.set_font("DejaVu", size=11)

    lines = optimized_text.split("\n")

    for raw_line in lines:
        stripped = raw_line.strip()

        if not stripped:
            pdf.ln(2)
            continue

        # Section divider line: a line that is just dashes -> draw a horizontal rule
        if re.fullmatch(r'-{2,}', stripped):
            pdf.set_x(pdf.l_margin)
            y = pdf.get_y()
            pdf.set_draw_color(180, 180, 180)
            pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
            pdf.ln(4)
            continue

        # Section header: short ALL-CAPS line -> bold, larger, with spacing before
        is_header = stripped.isupper() and 2 <= len(stripped) < 40 and any(c.isalpha() for c in stripped)

        if is_header:
            pdf.ln(3)
            pdf.set_font("DejaVu", "B", 13)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, 7, _sanitize(stripped))
            pdf.set_font("DejaVu", size=11)
            continue

        # Normal line: parse **bold** segments and render mixed bold/regular text
        pdf.set_x(pdf.l_margin)
        _render_line_with_bold(pdf, stripped)

    pdf.output(output_path)
    return output_path


def _render_line_with_bold(pdf, line, line_height=6):
    """
    Render a single line, switching between regular and bold font
    wherever **text** markers appear, using write() so segments flow
    on the same visual line instead of starting new cells.
    """
    line = _strip_other_markdown(line)
    segments = re.split(r'(\*\*.*?\*\*)', line)

    pdf.set_x(pdf.l_margin)
    page_width = pdf.w - pdf.l_margin - pdf.r_margin

    for seg in segments:
        if not seg:
            continue
        is_bold = seg.startswith("**") and seg.endswith("**") and len(seg) > 4
        text = _sanitize(seg[2:-2] if is_bold else seg)
        pdf.set_font("DejaVu", "B" if is_bold else "", 11)

        # If this segment doesn't fit on the remaining line width, wrap to a new line
        # BEFORE writing it, so a bold word never gets split mid-word.
        remaining_width = (pdf.w - pdf.r_margin) - pdf.get_x()
        seg_width = pdf.get_string_width(text)
        if seg_width > remaining_width and pdf.get_x() > pdf.l_margin:
            pdf.ln(line_height)
            pdf.set_x(pdf.l_margin)

        pdf.write(line_height, text)

    pdf.ln(line_height)


def _strip_other_markdown(text):
    # Remove markdown we don't want to render (headers, single-asterisk italics)
    text = re.sub(r'^#{1,6}\s*', '', text)
    text = re.sub(r'(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)', r'\1', text)  # strip single * italics
    return text