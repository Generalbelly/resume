"""Generate English resume PDF matching the existing styled layout."""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# Colors
GREEN = HexColor("#6aa84f")
BLACK = HexColor("#000000")
DARK_GRAY = HexColor("#666666")
LIGHT_GRAY = HexColor("#999999")

# Page
WIDTH, HEIGHT = letter
MARGIN_L = 55
MARGIN_R = 50
MARGIN_T = 55
MARGIN_B = 55

# Two-column layout
LABEL_X = MARGIN_L
CONTENT_X = 220
CONTENT_W = WIDTH - CONTENT_X - MARGIN_R


def wrap_text(c, text, font, size, max_width):
    """Word-wrap text into lines that fit within max_width."""
    c.setFont(font, size)
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip() if current else word
        if c.stringWidth(test, font, size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


class ResumeBuilder:
    def __init__(self, filename):
        self.c = canvas.Canvas(filename, pagesize=letter)
        self.y = HEIGHT - MARGIN_T
        self.first_page = True

    def _check_space(self, needed):
        if self.y - needed < MARGIN_B:
            self.c.showPage()
            self.y = HEIGHT - MARGIN_T
            self.first_page = False

    def draw_header(self):
        c = self.c
        y = self.y

        # Left: Large name
        c.setFont("Helvetica-Bold", 34)
        c.setFillColor(BLACK)
        c.drawString(LABEL_X, y, "Nobuyoshi")
        y -= 40
        c.drawString(LABEL_X, y, "Shimmen")
        y -= 26

        # "Engineer" in green
        c.setFont("Helvetica", 16)
        c.setFillColor(GREEN)
        c.drawString(LABEL_X, y, "Engineer")

        # Right: Contact info (offset to avoid overlapping the large name)
        contact_x = 330
        cy = self.y + 2
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(BLACK)
        c.drawString(contact_x, cy, "Nobuyoshi Shimmen")
        cy -= 15
        c.setFont("Helvetica", 9)
        c.setFillColor(DARK_GRAY)
        c.drawString(contact_x, cy, "116-0013 Tokyo, Arakawa-ku")
        cy -= 12
        c.drawString(contact_x, cy, "Nishinippori 6-10-14-501")
        cy -= 18
        c.setFillColor(BLACK)
        c.drawString(contact_x, cy, "070-4087-4039")
        cy -= 13
        c.drawString(contact_x, cy, "nobuyoshi.shimmen@gmail.com")

        self.y = y - 40

    def draw_section_label(self, label):
        """Draw section label on the left and green bar on the right."""
        self._check_space(40)

        # Dash line above label
        self.c.setStrokeColor(DARK_GRAY)
        self.c.setLineWidth(0.5)
        self.c.line(LABEL_X, self.y + 16, LABEL_X + 25, self.y + 16)

        # Label
        self.c.setFont("Helvetica-Bold", 13)
        self.c.setFillColor(BLACK)
        self.c.drawString(LABEL_X, self.y, label)

        # Green bar
        self.c.setFillColor(GREEN)
        self.c.rect(CONTENT_X, self.y + 14, CONTENT_W, 3, fill=1, stroke=0)

        self.y -= 8

    def draw_paragraph(self, text, font="Helvetica", size=9.8, color=BLACK, line_height=14):
        """Draw a wrapped paragraph in the content column."""
        lines = wrap_text(self.c, text, font, size, CONTENT_W)
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        for line in lines:
            self._check_space(line_height)
            self.c.drawString(CONTENT_X, self.y, line)
            self.y -= line_height

    def draw_spacer(self, height=8):
        self.y -= height

    def draw_experience(self, company, role, period, location, bullets):
        self._check_space(50)

        c = self.c

        # Company (bold) + role
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(BLACK)
        company_w = c.stringWidth(company, "Helvetica-Bold", 10.5)
        c.drawString(CONTENT_X, self.y, company)
        c.setFont("Helvetica", 10.5)
        c.drawString(CONTENT_X + company_w, self.y, f" / {role}")
        self.y -= 14

        # Period + location
        c.setFont("Helvetica", 8.5)
        c.setFillColor(LIGHT_GRAY)
        c.drawString(CONTENT_X, self.y, f"{period},  {location}")
        self.y -= 18

        # Bullets
        for bullet in bullets:
            self._check_space(16)
            lines = wrap_text(c, bullet, "Helvetica", 9.5, CONTENT_W - 12)
            c.setFont("Helvetica", 9.5)
            c.setFillColor(BLACK)
            for i, line in enumerate(lines):
                self._check_space(14)
                prefix = "\u2022" if i == 0 else "  "
                c.drawString(CONTENT_X, self.y, f"{prefix}{line}")
                self.y -= 14

        self.y -= 6

    def draw_education(self, school, detail, period, location, note=None):
        self._check_space(40)
        c = self.c

        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(BLACK)
        school_w = c.stringWidth(school, "Helvetica-Bold", 10.5)
        c.drawString(CONTENT_X, self.y, school)
        c.setFont("Helvetica", 10.5)
        c.drawString(CONTENT_X + school_w, self.y, f" / {detail}")
        self.y -= 14

        c.setFont("Helvetica", 8.5)
        c.setFillColor(LIGHT_GRAY)
        c.drawString(CONTENT_X, self.y, f"{period},  {location}")
        self.y -= 16

        if note:
            self._check_space(14)
            c.setFont("Helvetica", 9.5)
            c.setFillColor(BLACK)
            c.drawString(CONTENT_X, self.y, f"\u30fb{note}")
            self.y -= 14

        self.y -= 6

    def draw_skill_group(self, title, text):
        self._check_space(30)
        c = self.c

        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(BLACK)
        c.drawString(CONTENT_X, self.y, title)
        self.y -= 15

        lines = wrap_text(c, text, "Helvetica", 9.5, CONTENT_W)
        c.setFont("Helvetica", 9.5)
        c.setFillColor(BLACK)
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


def main():
    r = ResumeBuilder("/Users/nobuyoshishimmen/dev/resume/en/Resume.pdf")

    # ── Header ──
    r.draw_header()

    # ── About Me ──
    r.draw_section_label("About Me")
    r.draw_paragraph(
        'With a "let\'s just try it and build it" mentality honed over 10+ years '
        "at startups, I thrive on taking products from zero to one. I enjoy working "
        "collaboratively but can also effectively coordinate a project from start to "
        "finish independently."
    )
    r.draw_spacer(6)
    r.draw_paragraph(
        "I've learned firsthand that cutting corners on initial design leads to costly "
        "rework at scale, so I'm mindful of striking the right balance. I also recognize "
        "that sales, marketing, and customer support are all critical to getting a business "
        "on track, so I collaborate effectively with cross-functional teams while respecting "
        "everyone's contributions."
    )
    r.draw_spacer(6)
    r.draw_paragraph(
        "With the evolution of generative AI, MVPs can now be built many times faster "
        "than before, and I want to leverage that to the fullest to help people and "
        "create businesses that generate revenue."
    )
    r.draw_spacer(8)

    # ── Experience ──
    r.draw_section_label("Experience")

    r.draw_experience(
        "agito, Inc.",
        "PdM & Engineer",
        "OCT 2024 - NOV 2025",
        "TOKYO",
        [
            "Served as both PdM and engineer for new products, handling customer "
            "interviews, planning & development, and sales as a solo contributor",
            "Built a creative generation tool using generative AI to create ad banners "
            "and copy from landing page information",
            "Developed an ad campaign search tool enabling searches not possible with "
            "the existing product",
            "Built an ad campaign simulation tool that generates forecasts for new "
            "campaigns based on historical performance data",
            "Tech: TypeScript, PubSub, Cloud Run, Memorystore, Cloud Scheduler, "
            "BigQuery, Vertex AI (vector search)",
        ],
    )

    r.draw_experience(
        "agito, Inc.",
        "Product Manager",
        "JAN 2023 - JUL 2024",
        "TOKYO",
        [
            "Bridged business and engineering teams as PdM, driving core system "
            "renewal, feature improvements, and development process optimization",
            "Created and managed product roadmap; handled requirements definition "
            "and prioritization",
            "Managed engineering team of 8-10 (task assignment, progress tracking, "
            "new member onboarding)",
            "Led core system renewal enabling same-day data retrieval, "
            "differentiating from competitors",
            "Built Looker Studio integration using Linking API for instant report "
            "creation",
            "Developed beta features using GAS for customer needs (GA4, AppsFlyer, "
            "Adjust integrations)",
            "Coordinated incident response and feature releases with business team",
        ],
    )

    r.draw_experience(
        "agito, Inc.",
        "Tech Lead (Joined PLAID Group Oct 2022)",
        "SEPT 2018 - DEC 2022",
        "TOKYO",
        [
            "Founding member; built an ad reporting tool (data-be.at) from scratch "
            "leveraging BigQuery, serving as the CTO's right hand",
            "Led team of 3-5 engineers, handled business communication, requirements "
            "definition, and progress management",
            "Scaled connected ad accounts from 3,000 to 20,000 (ad reports acquired: "
            "~200,000/day across 20 ad platforms)",
            "Replaced existing ad report collection app with serverless architecture "
            "(Go, PubSub, Cloud Run, Datastore, BigQuery)",
            "Built data mart application linking ad data with customer data",
            "Developed SQL generation app for BI tools and Excel report generation app",
            "Built web application as full-stack developer (Vue.js/Vuetify, Laravel)",
            "Created a prototype for industry classification from ad text",
        ],
    )

    r.draw_experience(
        "ubun, Inc.",
        "Freelance Engineer",
        "FEB 2021 - APR 2022",
        "TOKYO",
        [
            "Developed an application targeted for Amazon sellers as a side project",
            "Responsible for front-end, back-end, and batch processing as a full "
            "stack developer",
        ],
    )

    r.draw_experience(
        "Techloco, Inc.",
        "Engineer (Seconded from Soldout, Inc.)",
        "OCT 2015 - JUL 2018",
        "TOKYO",
        [
            "Collaborated in developing brick, an all-in-one marketing tool",
            "Proposed and developed Site Review, a tool that enables reviewing, "
            "commenting on, and suggesting edits to website designs directly in "
            "the browser",
        ],
    )

    r.draw_experience(
        "Soldout, Inc.",
        "Marketing Division",
        "APR 2014 - SEP 2015",
        "TOKYO",
        [
            "Automated business workflows using GAS, Salesforce API, and "
            "HubSpot API, leveraging coding skills from building iOS apps as a hobby",
        ],
    )

    # ── Education ──
    r.draw_section_label("Education")

    r.draw_education(
        "Aoyama Gakuin University",
        "Bachelor of Business Administration, BBA",
        "APR 2010 - MAR 2014",
        "TOKYO",
    )

    r.draw_education(
        "The University of Vermont",
        "Concentration in Business",
        "AUG 2012 - MAY 2013",
        "BURLINGTON, VERMONT, USA",
        note="9-month exchange program through International Partnership & Collaboration",
    )

    # ── Projects ──
    r.draw_section_label("Projects")
    for url in [
        "https://www.data-be.at/",
        "https://markezine.jp/article/detail/26719",
        "https://www.brick.tools/",
    ]:
        r._check_space(16)
        r.c.setFont("Helvetica", 9.5)
        r.c.setFillColor(DARK_GRAY)
        r.c.drawString(CONTENT_X, r.y, url)
        r.y -= 16

    # ── Skills & Interests ──
    r.draw_section_label("Skills & Interests")

    r.draw_skill_group(
        "Computer Languages",
        "Proficient: Go, TypeScript/JavaScript, PHP, HTML/CSS, SQL   "
        "Frameworks: Node.js, Next.js, React, Vue, Laravel",
    )

    r.draw_skill_group(
        "Infrastructures",
        "GCP: Cloud Run, PubSub, Datastore, Memorystore, Cloud Scheduler, GAE, "
        "GCE, Cloud SQL, BigQuery, Cloud Storage, Cloud Monitoring, Cloud Logging, "
        "Cloud Build, Vertex AI, Firebase (personal), Cloud Functions (personal)   "
        "AWS: EC2, S3   Others: Docker, GitHub Actions, Circle CI, Git",
    )

    r.draw_skill_group(
        "Languages",
        "Native: Japanese   Business: English (TOEIC score 960)",
    )

    r.draw_skill_group(
        "Interests and Hobbies",
        "Building new products from scratch, leveraging generative AI for rapid "
        "prototyping, spending time with family, studying fitness and working out",
    )

    # ── Certificates ──
    r.draw_section_label("Certificates")
    r.draw_certificate("Udacity / Machine Learning Engineer Nanodegree", "2016 - 2017")
    r.draw_certificate("Udacity / iOS Engineer Nanodegree", "2015")

    # ── Links ──
    r.draw_section_label("Links")
    r.draw_link("Blog", "https://www.tumblr.com/blog/nobuyoshi-shimmen")
    r.draw_link("GitHub", "https://github.com/Generalbelly")
    r.draw_link("LinkedIn", "https://www.linkedin.com/in/nobuyoshi-shimmen-9a8b1a94/")

    r.save()
    print("Generated: en/Resume.pdf")


if __name__ == "__main__":
    main()
