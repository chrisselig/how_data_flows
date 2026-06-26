"""PDF certificate generator for Streamlit courses.

Simplified from SQL Quest — no tiers, no YAML config.
Single completion certificate per course using ReportLab.

Layout (A4 landscape = 841.89 x 595.28 pt):
  Top-right corner  : company logo placeholder
  Centre column     : title, course badge, name, body text, stats
  Bottom            : footer + cert ID

Requires: reportlab
"""

from __future__ import annotations

import hashlib
import io
import math
from dataclasses import dataclass, field
from datetime import date

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class CertificateData:
    """Runtime values for one certificate."""

    display_name: str
    course_title: str
    course_id: str
    lessons_completed: int
    total_lessons: int
    total_xp: int
    level_title: str
    level_icon: str
    accent_color: str = "#244C5A"
    body_text: str = ""
    footer_text: str = "People Analytics Training Program | HR Analytics Academy"
    completion_date: date = field(default_factory=date.today)

    def certificate_id(self) -> str:
        """Unique 8-char hex ID — deterministic per name + course + date."""
        raw = f"{self.display_name}-{self.course_id}-{self.completion_date.isoformat()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:8].upper()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def generate_certificate_pdf(data: CertificateData) -> bytes:
    """Generate a course completion certificate PDF and return raw bytes."""
    buf = io.BytesIO()
    _draw(buf, data)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _hex(s: str) -> colors.Color:
    s = s.lstrip("#")
    r, g, b = (int(s[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return colors.Color(r, g, b)


def _word_wrap(
    c: canvas.Canvas, text: str, font: str, size: float, max_w: float
) -> list[str]:
    """Break *text* into lines that each fit within *max_w* points."""
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        test = " ".join(current + [word])
        if c.stringWidth(test, font, size) <= max_w:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines or [""]


def _draw_mock_logo(
    c: canvas.Canvas, cx: float, cy: float, r: float, accent: str
) -> None:
    """Draw a hexagonal mock company logo centred at (cx, cy)."""
    pts = [
        (
            cx + r * math.cos(math.radians(60 * i - 30)),
            cy + r * math.sin(math.radians(60 * i - 30)),
        )
        for i in range(6)
    ]
    path = c.beginPath()
    path.moveTo(*pts[0])
    for p in pts[1:]:
        path.lineTo(*p)
    path.close()
    c.setFillColor(_hex(accent))
    c.drawPath(path, fill=1, stroke=0)

    ir = r * 0.72
    ipts = [
        (
            cx + ir * math.cos(math.radians(60 * i - 30)),
            cy + ir * math.sin(math.radians(60 * i - 30)),
        )
        for i in range(6)
    ]
    ipath = c.beginPath()
    ipath.moveTo(*ipts[0])
    for p in ipts[1:]:
        ipath.lineTo(*p)
    ipath.close()
    c.setFillColor(colors.white)
    c.drawPath(ipath, fill=1, stroke=0)

    c.setFillColor(_hex(accent))
    c.setFont("Helvetica-Bold", r * 0.55)
    c.drawCentredString(cx, cy - r * 0.18, "PA")

    c.setFont("Helvetica", r * 0.28)
    c.setFillColor(colors.Color(0.6, 0.6, 0.6))
    c.drawCentredString(cx, cy - r * 1.55, "YOUR LOGO")


# ---------------------------------------------------------------------------
# Main drawing function
# ---------------------------------------------------------------------------

# Shared color palette
_COLOR_BORDER = "#244C5A"
_COLOR_TITLE = "#244C5A"
_COLOR_BODY = "#244C5A"
_COLOR_STAT_BG = "#f8f6f0"
_COLOR_STAT_VALUE = "#244C5A"
_COLOR_STAT_LABEL = "#6BA4B8"
_COLOR_FOOTER = "#6BA4B8"
_COLOR_NAME = "#244C5A"


def _draw(buf: io.BytesIO, data: CertificateData) -> None:
    """Render the complete certificate to *buf*."""
    page = landscape(A4)
    W, H = page
    c = canvas.Canvas(buf, pagesize=page)
    c.setTitle(f"{data.course_title} — Certificate — {data.display_name}")

    m = 16 * mm
    pad = m * 0.5
    inset = pad + 7
    accent = data.accent_color

    logo_col_w = 32 * mm
    logo_margin = 10
    content_w = W - 2 * inset - logo_col_w - logo_margin
    content_cx = inset + content_w / 2

    # -- Background -----------------------------------------------------------
    c.setFillColor(colors.white)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Subtle parchment tint
    c.setFillColor(colors.Color(0.995, 0.992, 0.978, alpha=0.6))
    c.rect(pad + 1, pad + 1, W - 2 * pad - 2, H - 2 * pad - 2, fill=1, stroke=0)

    # -- Outer border ---------------------------------------------------------
    c.setStrokeColor(_hex(_COLOR_BORDER))
    c.setLineWidth(5)
    c.rect(pad, pad, W - 2 * pad, H - 2 * pad, fill=0, stroke=1)

    # -- Inner accent border --------------------------------------------------
    c.setStrokeColor(_hex(accent))
    c.setLineWidth(1.8)
    c.rect(inset, inset, W - 2 * inset, H - 2 * inset, fill=0, stroke=1)

    # -- Corner diamonds ------------------------------------------------------
    c.setFillColor(_hex(accent))
    sq = 5
    for ox, oy in [
        (inset - sq / 2, inset - sq / 2),
        (W - inset - sq / 2, inset - sq / 2),
        (inset - sq / 2, H - inset - sq / 2),
        (W - inset - sq / 2, H - inset - sq / 2),
    ]:
        c.saveState()
        c.translate(ox + sq / 2, oy + sq / 2)
        c.rotate(45)
        c.rect(-sq / 2, -sq / 2, sq, sq, fill=1, stroke=0)
        c.restoreState()

    # -- Logo (top-right) -----------------------------------------------------
    logo_inset_r = 14
    logo_inset_t = 12
    logo_cx = W - inset - logo_inset_r - logo_col_w / 2
    logo_cy = H - inset - logo_inset_t - logo_col_w * 0.45
    logo_r = logo_col_w * 0.34
    _draw_mock_logo(c, logo_cx, logo_cy, logo_r, accent)

    # -- Vertical cursor ------------------------------------------------------
    y = H - inset - 18

    # -- Title ----------------------------------------------------------------
    title_size = 26
    y -= title_size
    c.setFillColor(_hex(_COLOR_TITLE))
    c.setFont("Times-Bold", title_size)
    c.drawCentredString(content_cx, y, "CERTIFICATE OF COMPLETION")

    lw = content_w * 0.65
    c.setStrokeColor(_hex(accent))
    c.setLineWidth(1.5)
    c.line(content_cx - lw / 2, y - 6, content_cx + lw / 2, y - 6)
    y -= title_size * 0.5

    # -- Program name ---------------------------------------------------------
    prog_size = 12
    y -= prog_size + 4
    c.setFillColor(_hex(_COLOR_BODY))
    c.setFont("Times-Italic", prog_size)
    c.drawCentredString(content_cx, y, f"{data.course_title} — HR Analytics Academy")

    # -- Course badge pill ----------------------------------------------------
    y -= 20
    badge_text = f"  {data.course_title}  "
    bs = 8.5
    c.setFont("Helvetica-Bold", bs)
    bw = c.stringWidth(badge_text, "Helvetica-Bold", bs) + 22
    bh = 15
    bx = content_cx - bw / 2
    by = y - bh + 3
    c.setFillColor(_hex(accent))
    c.roundRect(bx, by, bw, bh, bh / 2, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.drawCentredString(content_cx, by + 4.5, badge_text)

    y -= bh + 4
    c.setFont("Helvetica", 8.5)
    c.setFillColor(_hex(accent))
    c.drawCentredString(content_cx, y, "Course Completed")

    # -- Thin divider ---------------------------------------------------------
    y -= 14
    dw = content_w * 0.4
    c.setStrokeColor(_hex(accent))
    c.setLineWidth(0.5)
    c.line(content_cx - dw / 2, y, content_cx + dw / 2, y)

    # -- "This is to certify that" --------------------------------------------
    y -= 20
    c.setFont("Helvetica", 10)
    c.setFillColor(_hex(_COLOR_BODY))
    c.drawCentredString(content_cx, y, "This is to certify that")

    # -- Participant name (hero element) --------------------------------------
    name_size = 34
    y -= name_size + 6
    c.setFont("Times-BoldItalic", name_size)
    c.setFillColor(_hex(_COLOR_NAME))
    c.drawCentredString(content_cx, y, data.display_name)

    nw = c.stringWidth(data.display_name, "Times-BoldItalic", name_size)
    c.setStrokeColor(_hex(accent))
    c.setLineWidth(1)
    c.line(content_cx - nw / 2, y - 4, content_cx + nw / 2, y - 4)
    y -= 10

    # -- Body text ------------------------------------------------------------
    body_font = "Helvetica"
    body_size = 11
    body_lh = body_size + 4
    max_body_w = content_w * 0.88

    raw_body = " ".join(data.body_text.split()) if data.body_text else (
        f"has successfully completed all {data.total_lessons} lessons in "
        f"{data.course_title}, demonstrating knowledge of the concepts and "
        f"skills covered in this course."
    )
    body_lines = _word_wrap(c, raw_body, body_font, body_size, max_body_w)

    c.setFont(body_font, body_size)
    c.setFillColor(_hex(_COLOR_BODY))
    for line in body_lines:
        y -= body_lh
        c.drawCentredString(content_cx, y, line)

    # -- Stats row ------------------------------------------------------------
    y -= 26
    stats: list[tuple[str, str]] = [
        (f"{data.lessons_completed}/{data.total_lessons}", "Lessons"),
        (f"{data.total_xp:,} XP", "Total Score"),
        (data.completion_date.strftime("%d %b %Y"), "Completed"),
        (data.level_title, "Level Achieved"),
    ]

    gap = 12
    n = len(stats)
    stat_margin = 20
    box_h = 40
    full_row_w = W - 2 * inset - 2 * stat_margin
    box_w = (full_row_w - gap * (n - 1)) / n
    sx = inset + stat_margin

    stat_top_y = y
    by_box = stat_top_y - box_h

    for i, (val, label) in enumerate(stats):
        bx = sx + i * (box_w + gap)
        c.setFillColor(_hex(_COLOR_STAT_BG))
        c.setStrokeColor(_hex(accent))
        c.setLineWidth(0.8)
        c.roundRect(bx, by_box, box_w, box_h, 4, fill=1, stroke=1)

        val_font_size = 17
        val_font = "Helvetica-Bold"
        while c.stringWidth(val, val_font, val_font_size) > box_w - 8 and val_font_size > 9:
            val_font_size -= 1
        c.setFont(val_font, val_font_size)
        c.setFillColor(_hex(_COLOR_STAT_VALUE))
        c.drawCentredString(bx + box_w / 2, by_box + box_h - val_font_size - 4, val)

        c.setFont("Helvetica", 9)
        c.setFillColor(_hex(_COLOR_STAT_LABEL))
        c.drawCentredString(bx + box_w / 2, by_box + 7, label.upper())

    y = by_box - 20

    # -- Decorative divider below stats ---------------------------------------
    dw2 = content_w * 0.3
    c.setStrokeColor(_hex(accent))
    c.setLineWidth(0.5)
    c.line(content_cx - dw2 / 2, y, content_cx + dw2 / 2, y)

    # -- Motivational closing text --------------------------------------------
    y -= 18
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(_hex(_COLOR_BODY))
    c.drawCentredString(
        content_cx, y, "Keep learning, keep growing — your data journey continues."
    )

    # -- Certificate ID -------------------------------------------------------
    c.setFont("Courier", 7)
    c.setFillColor(_hex(_COLOR_FOOTER))
    c.drawString(inset + 4, inset + 6, f"Certificate ID: {data.certificate_id()}")

    # -- Footer ---------------------------------------------------------------
    c.setFont("Helvetica", 8)
    c.setFillColor(_hex(_COLOR_FOOTER))
    c.drawCentredString(W / 2, inset + 6, data.footer_text)

    c.save()
