"""Generate both en/README.md and en/Resume.pdf from en/resume.yaml."""

import os
from pathlib import Path

import yaml
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).parent

# ─── Date formatting ───────────────────────────────────────────────

MONTHS = {
    1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN",
    7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC",
}


def _parse_date(date_str):
    year, month = date_str.split("-")
    return int(year), int(month)


def fmt_date_readme(date_str):
    """'2024-10' → '2024/10'"""
    year, month = _parse_date(date_str)
    return f"{year}/{month:02d}"


def fmt_date_pdf(date_str):
    """'2024-10' → 'OCT 2024'"""
    year, month = _parse_date(date_str)
    return f"{MONTHS[month]} {year}"


# ─── Load data ─────────────────────────────────────────────────────

def load_data():
    with open(BASE_DIR / "resume.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ═══════════════════════════════════════════════════════════════════
# README generation
# ═══════════════════════════════════════════════════════════════════

def generate_readme(data):
    lines = []

    def w(text=""):
        lines.append(text)

    # Header
    w("# Resume")
    w()
    w("Japanese version is [available](../README.md)")
    w()

    # Skills
    w("## Skills")
    w()
    w("### Languages")
    w()
    sk = data["skills"]
    proficient = ", ".join(sk["programming"]["proficient"])
    frameworks = ", ".join(sk["programming"]["frameworks"])
    w(f"- {proficient}")
    w(f"- Frameworks: {frameworks}")
    for lang in sk["human_languages"]:
        w(f"- {lang['language']} - {lang['level']}")
    w()

    w("### Infrastructure")
    w()
    infra = sk["infrastructure"]
    for provider in ["gcp", "aws"]:
        if provider in infra:
            w(f"- {provider.upper()}")
            for svc in infra[provider]:
                w(f"  - {svc}")
    if "ci_cd" in infra:
        w("- CI/CD")
        for svc in infra["ci_cd"]:
            w(f"  - {svc}")
    if "other" in infra:
        w("- Other")
        for svc in infra["other"]:
            w(f"  - {svc}")
    w()

    # Strengths
    w("## Strengths")
    w()
    for i, para in enumerate(data["about"]["strengths"]):
        w(para)
        if i < len(data["about"]["strengths"]) - 1:
            w()
    w()

    # About Me as an Engineer
    w("## About Me as an Engineer")
    w()
    for trait in data["about"]["engineer_traits"]:
        w(f"- {trait['title']}")
        w(f"  - {trait['detail']}")
    w()

    # Links
    w("## Links")
    w()
    for link in data["links"]:
        w(f"- [{link['label']}]({link['url']})")
    w()

    # Work Experience
    w("## Work Experience")
    w()
    for exp in data["experience"]:
        period = f"{fmt_date_readme(exp['start'])} - {fmt_date_readme(exp['end'])}"
        role_suffix = f" ({exp['role_note']})" if exp.get("role_note") else ""
        w(f"### {period} : {exp['company']}{role_suffix}")
        w()
        w(exp["description"])
        w()

        if exp.get("responsibilities"):
            w("Responsibilities")
            w()
            for r in exp["responsibilities"]:
                w(f"- {r}")
            w()

        if exp.get("team"):
            w("Team Size")
            w()
            for t in exp["team"]:
                w(f"- {t}")
            w()

        if exp.get("product_scale"):
            w("Product Scale")
            w()
            for ps in exp["product_scale"]:
                w(f"- {ps}")
            w()

        if exp.get("projects"):
            w("Projects")
            w()
            for proj in exp["projects"]:
                w(f"- {proj['name']}")
                if proj.get("detail"):
                    w(f"  - {proj['detail']}")
                if proj.get("tech"):
                    w(f"  - Tech stack: {proj['tech']}")
            w()

        if exp.get("tech"):
            w(f"- Tech stack: {exp['tech']}")
            w()

        if exp.get("outside_work"):
            w("Outside of work")
            w()
            for item in exp["outside_work"]:
                w(f"- {item}")
            w()

    # Education
    w("## Education")
    w()
    for edu in data["education"]:
        period = f"{fmt_date_readme(edu['start'])} - {fmt_date_readme(edu['end'])}"
        w(f"- **{edu['school']}** - {edu['degree']} ({period}, {edu['location']})")
        if edu.get("note"):
            w(f"  - {edu['note']}")
    w()

    readme_path = BASE_DIR / "README.md"
    readme_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated: {readme_path.relative_to(BASE_DIR.parent)}")


# ═══════════════════════════════════════════════════════════════════
# PDF generation
# ═══════════════════════════════════════════════════════════════════

GREEN = HexColor("#6aa84f")
BLACK = HexColor("#000000")
DARK_GRAY = HexColor("#666666")
LIGHT_GRAY = HexColor("#999999")

WIDTH, HEIGHT = letter
MARGIN_L = 55
MARGIN_R = 50
MARGIN_T = 55
MARGIN_B = 55

LABEL_X = MARGIN_L
CONTENT_X = 220
CONTENT_W = WIDTH - CONTENT_X - MARGIN_R


def _wrap_text(c, text, font, size, max_width):
    c.setFont(font, size)
    words = text.split(" ")
    result = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip() if current else word
        if c.stringWidth(test, font, size) <= max_width:
            current = test
        else:
            if current:
                result.append(current)
            current = word
    if current:
        result.append(current)
    return result


class _ResumeBuilder:
    def __init__(self, filename):
        self.c = canvas.Canvas(str(filename), pagesize=letter)
        self.y = HEIGHT - MARGIN_T

    def _check_space(self, needed):
        if self.y - needed < MARGIN_B:
            self.c.showPage()
            self.y = HEIGHT - MARGIN_T

    def draw_header(self, data):
        c = self.c
        y = self.y

        first, last = data["name"].split(" ", 1)
        c.setFont("Helvetica-Bold", 34)
        c.setFillColor(BLACK)
        c.drawString(LABEL_X, y, first)
        y -= 40
        c.drawString(LABEL_X, y, last)
        y -= 26

        c.setFont("Helvetica", 16)
        c.setFillColor(GREEN)
        c.drawString(LABEL_X, y, data["title"])

        contact = data["contact"]
        cx = 330
        cy = self.y + 2
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(BLACK)
        c.drawString(cx, cy, data["name"])
        cy -= 15
        c.setFont("Helvetica", 9)
        c.setFillColor(DARK_GRAY)
        c.drawString(cx, cy, contact["address_line1"])
        cy -= 12
        c.drawString(cx, cy, contact["address_line2"])
        cy -= 18
        c.setFillColor(BLACK)
        c.drawString(cx, cy, contact["phone"])
        cy -= 13
        c.drawString(cx, cy, contact["email"])

        self.y = y - 40

    def draw_section_label(self, label):
        self._check_space(40)
        self.c.setStrokeColor(DARK_GRAY)
        self.c.setLineWidth(0.5)
        self.c.line(LABEL_X, self.y + 16, LABEL_X + 25, self.y + 16)

        self.c.setFont("Helvetica-Bold", 13)
        self.c.setFillColor(BLACK)
        self.c.drawString(LABEL_X, self.y, label)

        self.c.setFillColor(GREEN)
        self.c.rect(CONTENT_X, self.y + 14, CONTENT_W, 3, fill=1, stroke=0)
        self.y -= 8

    def draw_paragraph(self, text):
        lines = _wrap_text(self.c, text, "Helvetica", 9.8, CONTENT_W)
        self.c.setFont("Helvetica", 9.8)
        self.c.setFillColor(BLACK)
        for line in lines:
            self._check_space(14)
            self.c.drawString(CONTENT_X, self.y, line)
            self.y -= 14

    def draw_spacer(self, height=8):
        self.y -= height

    def draw_bullets(self, items):
        c = self.c
        for item in items:
            self._check_space(16)
            wrapped = _wrap_text(c, item, "Helvetica", 9.5, CONTENT_W - 12)
            c.setFont("Helvetica", 9.5)
            c.setFillColor(BLACK)
            for i, line in enumerate(wrapped):
                self._check_space(14)
                prefix = "\u2022" if i == 0 else " "
                c.drawString(CONTENT_X, self.y, f"{prefix}{line}")
                self.y -= 14

    def draw_experience(self, company, role, period, location, bullets):
        self._check_space(50)
        c = self.c

        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(BLACK)
        cw = c.stringWidth(company, "Helvetica-Bold", 10.5)
        c.drawString(CONTENT_X, self.y, company)
        c.setFont("Helvetica", 10.5)
        c.drawString(CONTENT_X + cw, self.y, f" / {role}")
        self.y -= 14

        c.setFont("Helvetica", 8.5)
        c.setFillColor(LIGHT_GRAY)
        c.drawString(CONTENT_X, self.y, f"{period},  {location}")
        self.y -= 18

        self.draw_bullets(bullets)
        self.y -= 6

    def draw_education(self, school, detail, period, location, note=None):
        self._check_space(40)
        c = self.c

        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(BLACK)
        sw = c.stringWidth(school, "Helvetica-Bold", 10.5)
        c.drawString(CONTENT_X, self.y, school)
        c.setFont("Helvetica", 10.5)
        c.drawString(CONTENT_X + sw, self.y, f" / {detail}")
        self.y -= 14

        c.setFont("Helvetica", 8.5)
        c.setFillColor(LIGHT_GRAY)
        c.drawString(CONTENT_X, self.y, f"{period},  {location}")
        self.y -= 16

        if note:
            self._check_space(14)
            self.draw_bullets([note])
        self.y -= 6

    def draw_skill_group(self, title, text):
        self._check_space(30)
        c = self.c
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(BLACK)
        c.drawString(CONTENT_X, self.y, title)
        self.y -= 15

        lines = _wrap_text(c, text, "Helvetica", 9.5, CONTENT_W)
        c.setFont("Helvetica", 9.5)
        for line in lines:
            self._check_space(13)
            c.drawString(CONTENT_X, self.y, line)
            self.y -= 13
        self.y -= 10

    def draw_certificate(self, name, year):
        self._check_space(28)
        c = self.c
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(BLACK)
        c.drawString(CONTENT_X, self.y, name)
        self.y -= 13
        c.setFont("Helvetica", 8.5)
        c.setFillColor(LIGHT_GRAY)
        c.drawString(CONTENT_X, self.y, year)
        self.y -= 18

    def draw_link(self, label, url):
        self._check_space(28)
        c = self.c
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(BLACK)
        c.drawString(CONTENT_X, self.y, label)
        self.y -= 14
        c.setFont("Helvetica", 9)
        c.setFillColor(DARK_GRAY)
        c.drawString(CONTENT_X + 10, self.y, url)
        self.y -= 16

    def save(self):
        self.c.save()


def _build_pdf_bullets(exp):
    """Derive PDF bullet points from structured experience data."""
    bullets = [exp["description"]]
    for proj in exp.get("projects", []):
        if proj.get("detail"):
            bullets.append(proj["detail"])
        else:
            # Use project name as bullet, with tech if available
            text = proj["name"]
            if proj.get("tech"):
                text = f"{text} ({proj['tech']})"
            bullets.append(text)
    if exp.get("tech"):
        bullets.append(f"Tech: {exp['tech']}")
    return bullets


def _build_pdf_skills(skills):
    """Derive PDF skill group strings from structured skill data."""
    prog = skills["programming"]
    proficient = ", ".join(prog["proficient"])
    frameworks = ", ".join(prog["frameworks"])

    infra = skills["infrastructure"]
    infra_parts = []
    for provider in ["gcp", "aws"]:
        if provider in infra:
            infra_parts.append(f"{provider.upper()}: {', '.join(infra[provider])}")
    extras = []
    for key in ["ci_cd", "other"]:
        if key in infra:
            extras.extend(infra[key])
    if extras:
        infra_parts.append(f"Others: {', '.join(extras)}")

    langs = skills["human_languages"]
    lang_text = "   ".join(f"{l['level']}: {l['language']}" for l in langs)
    # Flip to "Native: Japanese   Business: English (TOEIC score 960)" style
    lang_parts = []
    for l in langs:
        level = l["level"].split(",")[0]  # "Business level, TOEIC 960" → "Business level"
        extra = ""
        if "TOEIC" in l["level"]:
            toeic = l["level"].split("TOEIC")[1].strip().rstrip(")")
            extra = f" (TOEIC score {toeic})"
        lang_parts.append(f"{level}: {l['language']}{extra}")
    lang_text = "   ".join(lang_parts)

    interests = ", ".join(skills.get("interests", []))

    return [
        ("Computer Languages", f"Proficient: {proficient}   Frameworks: {frameworks}"),
        ("Infrastructures", "   ".join(infra_parts)),
        ("Languages", lang_text),
        ("Interests and Hobbies", interests),
    ]


def generate_pdf(data):
    pdf_path = BASE_DIR / "Resume.pdf"
    r = _ResumeBuilder(pdf_path)

    # Header
    r.draw_header(data)

    # About Me
    r.draw_section_label("About Me")
    for para in data["about"]["strengths"]:
        r.draw_paragraph(para)
        r.draw_spacer(6)
    # Third paragraph from engineer traits
    trait = data["about"]["engineer_traits"][0]
    r.draw_paragraph(
        f"{trait['detail']}, to help people and create businesses that "
        "generate revenue."
    )
    r.draw_spacer(8)

    # Experience
    r.draw_section_label("Experience")
    for exp in data["experience"]:
        period = f"{fmt_date_pdf(exp['start'])} - {fmt_date_pdf(exp['end'])}"
        role = exp["role"]
        if exp.get("role_note"):
            role = f"{role} ({exp['role_note']})"
        bullets = _build_pdf_bullets(exp)
        r.draw_experience(exp["company"], role, period, exp["location"], bullets)

    # Education
    r.draw_section_label("Education")
    for edu in data["education"]:
        period = f"{fmt_date_pdf(edu['start'])} - {fmt_date_pdf(edu['end'])}"
        r.draw_education(
            edu["school"], edu["degree"], period,
            edu["location"].upper(), edu.get("note"),
        )

    # Projects
    r.draw_section_label("Projects")
    for proj in data["projects"]:
        r._check_space(16)
        r.c.setFont("Helvetica", 9.5)
        r.c.setFillColor(DARK_GRAY)
        r.c.drawString(CONTENT_X, r.y, proj["url"])
        r.y -= 16

    # Skills
    r.draw_section_label("Skills & Interests")
    for title, text in _build_pdf_skills(data["skills"]):
        r.draw_skill_group(title, text)

    # Certificates
    r.draw_section_label("Certificates")
    for cert in data["certificates"]:
        r.draw_certificate(cert["name"], cert["year"])

    # Links
    r.draw_section_label("Links")
    for link in data["links"]:
        r.draw_link(link["label"], link["url"])

    r.save()
    print(f"Generated: {pdf_path.relative_to(BASE_DIR.parent)}")


# ═══════════════════════════════════════════════════════════════════

def main():
    data = load_data()
    generate_readme(data)
    generate_pdf(data)


if __name__ == "__main__":
    main()
