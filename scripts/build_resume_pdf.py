from pathlib import Path
from textwrap import wrap
from xml.etree import ElementTree as ET

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Eric_Lane_AI_Automation_Consultant_Resume_With_QR.pdf"
QR_SVG = ROOT / "portfolio-qr.svg"
PORTFOLIO_URL = "https://ericlane87.github.io/Eric-Lane/"

W, H = letter

INK = colors.HexColor("#17202a")
MUTED = colors.HexColor("#5b6573")
ACCENT = colors.HexColor("#0f6b63")
ACCENT_DARK = colors.HexColor("#0b403c")
GOLD = colors.HexColor("#b7791f")
RULE = colors.HexColor("#d8e0e7")
SOFT = colors.HexColor("#eef6f4")
SIDEBAR = colors.HexColor("#f4f8f7")
WHITE = colors.white


def fit_lines(text, font, size, max_width):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        candidate = word if not line else f"{line} {word}"
        if stringWidth(candidate, font, size) <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(c, text, x, y, max_width, font="Helvetica", size=8, leading=10, color=INK):
    c.setFillColor(color)
    c.setFont(font, size)
    for line in fit_lines(text, font, size, max_width):
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_section_label(c, label, x, y, width, dark=False):
    c.setFillColor(WHITE if dark else ACCENT_DARK)
    c.setFont("Helvetica-Bold", 8.6)
    c.drawString(x, y, label.upper())
    c.setStrokeColor(colors.HexColor("#79aaa4") if dark else RULE)
    c.setLineWidth(0.7)
    c.line(x, y - 4, x + width, y - 4)
    return y - 15


def draw_bullet(c, text, x, y, max_width, size=7.75, leading=9.4, color=INK):
    c.setFillColor(color)
    c.setFont("Helvetica", size)
    lines = fit_lines(text, "Helvetica", size, max_width - 10)
    if not lines:
        return y
    c.drawString(x, y, "-")
    c.drawString(x + 9, y, lines[0])
    y -= leading
    for line in lines[1:]:
        c.drawString(x + 9, y, line)
        y -= leading
    return y + 1


def draw_qr(c, x, y, size):
    c.setFillColor(WHITE)
    c.rect(x, y, size, size, stroke=0, fill=1)
    root = ET.parse(QR_SVG).getroot()
    ns = {"svg": "http://www.w3.org/2000/svg"}
    scale = 1.763889
    view = 160.0
    c.setFillColor(colors.black)
    for rect in root.findall(".//svg:rect", ns):
        if "rgb(0%,0%,0%)" not in rect.attrib.get("style", ""):
            continue
        rx = float(rect.attrib["x"]) * scale / view * size
        ry = float(rect.attrib["y"]) * scale / view * size
        rw = float(rect.attrib["width"]) * scale / view * size
        rh = float(rect.attrib["height"]) * scale / view * size
        c.rect(x + rx, y + ry, rw, rh, stroke=0, fill=1)
    c.linkURL(PORTFOLIO_URL, (x - 2, y - 2, x + size + 2, y + size + 2), relative=0, thickness=0)


def draw_metric_card(c, x, y, w, h, number, label):
    c.setFillColor(WHITE)
    c.roundRect(x, y, w, h, 4, stroke=0, fill=1)
    c.setStrokeColor(RULE)
    c.roundRect(x, y, w, h, 4, stroke=1, fill=0)
    c.setFillColor(ACCENT_DARK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x + 10, y + h - 18, number)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.9)
    ty = y + h - 30
    for line in fit_lines(label, "Helvetica", 6.9, w - 18):
        c.drawString(x + 10, ty, line)
        ty -= 8


def main():
    c = canvas.Canvas(str(OUT), pagesize=letter)

    margin = 0.42 * inch
    sidebar_w = 2.06 * inch
    sidebar_x = margin
    main_x = sidebar_x + sidebar_w + 0.28 * inch
    main_w = W - main_x - margin

    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(ACCENT_DARK)
    c.rect(0, 0, 0.13 * inch, H, stroke=0, fill=1)
    c.setFillColor(SIDEBAR)
    c.roundRect(sidebar_x, margin, sidebar_w, H - 2 * margin, 7, stroke=0, fill=1)

    y = H - 0.47 * inch
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(main_x, y, "Eric Lane")
    y -= 18
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(main_x, y, "AI Automation & Digital Transformation Leader")
    y -= 14
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.4)
    c.drawString(main_x, y, "Operator + consultant + hands-on builder for enterprise automation programs")

    sy = H - 0.56 * inch
    c.setFillColor(ACCENT_DARK)
    c.setFont("Helvetica-Bold", 8.8)
    c.drawString(sidebar_x + 14, sy, "CONTACT")
    sy -= 14
    for line in ["Charlotte, NC", "ericlane87@gmail.com", "linkedin.com/in/eric-lane-m-s-747507131"]:
        sy = draw_wrapped(c, line, sidebar_x + 14, sy, sidebar_w - 28, size=7.2, leading=9, color=MUTED)
    sy -= 7
    draw_qr(c, sidebar_x + 14, sy - 58, 58)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 6.6)
    c.drawString(sidebar_x + 80, sy - 22, "Automation")
    c.drawString(sidebar_x + 80, sy - 31, "Portfolio")
    sy -= 79
    sy = draw_section_label(c, "Best Fit", sidebar_x + 14, sy, sidebar_w - 28)
    for line in ["Digital Transformation Leader", "AI Automation Consultant", "UiPath / RPA Consultant", "Operations Automation Lead", "Automation Enablement Manager"]:
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 7.4)
        c.drawString(sidebar_x + 14, sy, line)
        sy -= 11
    sy -= 7
    sy = draw_section_label(c, "Tool Stack", sidebar_x + 14, sy, sidebar_w - 28)
    for line in wrap("UiPath, RPA, OCR, Python, SQL, C#, .NET, VBA, Excel macros, automation scripts, ETL recovery, workflow documentation, Agile, SDLC", 28):
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7.25)
        c.drawString(sidebar_x + 14, sy, line)
        sy -= 9
    sy -= 8
    sy = draw_section_label(c, "Credentials", sidebar_x + 14, sy, sidebar_w - 28)
    for line in [
        "Certified UiPath Developer",
        "Decisions Certification",
        "M.S. Information Systems, Aspen",
        "B.S. Computer Science, ECPI",
        "A.S. Cyber & Network Security, ECPI",
    ]:
        sy = draw_bullet(c, line, sidebar_x + 14, sy, sidebar_w - 28, size=7.05, leading=8.5, color=MUTED)

    y = H - 1.20 * inch
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(main_x, y, "SELECTED BUSINESS IMPACT")
    y -= 11
    draw_metric_card(c, main_x, y - 45, main_w * 0.245, 42, "$6.8M", "consultant-led automation savings")
    draw_metric_card(c, main_x + main_w * 0.255, y - 45, main_w * 0.245, 42, "15+", "automation opportunities managed")
    draw_metric_card(c, main_x + main_w * 0.51, y - 45, main_w * 0.235, 42, "600+", "employees represented")
    draw_metric_card(c, main_x + main_w * 0.755, y - 45, main_w * 0.245, 42, "90%", "operational inventory reduction")
    y -= 64

    y = draw_section_label(c, "Executive Profile", main_x, y, main_w)
    profile = (
        "Digital transformation and AI automation leader who can discover the problem, build the solution, and drive adoption. "
        "Known for standing up automation functions, converting operational friction into practical UiPath, OCR, macro, SQL, and Python solutions, "
        "and packaging delivery with playbooks, training, governance, and measurable business cases."
    )
    y = draw_wrapped(c, profile, main_x, y, main_w, size=8.65, leading=10.9, color=INK)
    y -= 10

    y = draw_section_label(c, "Signature Value", main_x, y, main_w)
    for value in [
        ("Consultant mindset", "frames ambiguous work, runs discovery, defines ROI, writes LOEs, and builds roadmaps leaders can act on."),
        ("Builder credibility", "codes and implements practical automation across UiPath, VBA/macros, SQL, Python, OCR, and reporting workflows."),
        ("Operator experience", "understands queues, inventory pressure, SLA recovery, team enablement, governance, and sustained adoption.")
    ]:
        c.setFillColor(ACCENT_DARK)
        c.setFont("Helvetica-Bold", 8.55)
        c.drawString(main_x, y, value[0])
        y = draw_wrapped(c, value[1], main_x + 96, y, main_w - 96, size=7.95, leading=9.8, color=INK)
        y -= 2
    y -= 6

    y = draw_section_label(c, "Professional Experience", main_x, y, main_w)
    c.setFillColor(ACCENT_DARK)
    c.setFont("Helvetica-Bold", 9.3)
    c.drawString(main_x, y, "Elevance Health, formerly Anthem Inc.")
    y -= 13

    roles = [
        (
            "AI and Automation Consultant",
            "Nov 2024 to Present",
            [
                "Created a new AI and automation consulting function for enterprise operations, covering discovery, prioritization, documentation, delivery, and adoption.",
                "Supported leaders and operational groups representing 600+ employees while managing a 15+ opportunity portfolio and quarterly automation roadmaps.",
                "Authored an operations automation playbook covering intake, value calculation, LOE templates, governance gates, launch readiness, retrospectives, and continuous improvement.",
                "Delivered $6.8M in consultant-led savings, eliminated 140+ manual hours, and built UiPath enablement resources that reduced new developer onboarding by 20+ hours.",
            ],
        ),
        (
            "Manager, Payment Integrity",
            "Nov 2023 to Nov 2024",
            [
                "Built and scaled an operations team, hiring more than 95% of staff and creating the operating structure, policies, documentation, and coaching model.",
                "Implemented AI and automation improvements that reduced inventory by 90% and exceeded financial targets: $18M vs. $15M year one and $8M vs. $5M year two.",
            ],
        ),
        (
            "Software Engineer",
            "Anthem Inc. / Elevance Health",
            [
                "Built internal tools in .NET, C#, SQL, and Python to automate claims workflows, ETL recovery, diagnostics, operational support, and monitoring.",
            ],
        ),
        (
            "System Analyst",
            "Anthem Inc. / Elevance Health",
            [
                "Analyzed system issues, documented requirements, validated data flows, and improved operational reporting and support processes.",
            ],
        ),
    ]

    for title, dates, bullets in roles:
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 9.35)
        c.drawString(main_x, y, title)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7.75)
        c.drawRightString(main_x + main_w, y, dates)
        y -= 11
        for bullet in bullets:
            y = draw_bullet(c, bullet, main_x, y, main_w, size=7.7, leading=9.35)
        y -= 5

    c.save()


if __name__ == "__main__":
    main()
