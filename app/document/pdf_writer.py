from pathlib import Path
from datetime import date

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


def create_cover_letter_pdf(
    output_path: Path,
    candidate,
    job,
    cover_letter,
) -> None:

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=25 * mm,
        leftMargin=25 * mm,
        topMargin=22 * mm,
        bottomMargin=22 * mm,
        title="Cover Letter",
        author=candidate.name,
    )

    styles = getSampleStyleSheet()

    body_style = ParagraphStyle(
        "CoverLetterBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=16,
        alignment=TA_LEFT,
        spaceAfter=10,
    )

    greeting_style = ParagraphStyle(
        "CoverLetterGreeting",
        parent=body_style,
        spaceAfter=14,
    )

    closing_style = ParagraphStyle(
        "CoverLetterClosing",
        parent=body_style,
        spaceBefore=8,
        spaceAfter=4,
    )

    signoff_style = ParagraphStyle(
        "CoverLetterSignoff",
        parent=body_style,
        spaceAfter=2,
    )

    header_style = ParagraphStyle(
        "CoverLetterHeader",
        parent=body_style,
        leading=13,
        spaceAfter=0,
    )

    story = []

    header_lines = [
        candidate.name,
        candidate.address,
        candidate.phone,
        candidate.email,
        date.today().strftime("%d %B %Y"),
        "Hiring Manager",
        job.company,
    ]

    for index, line in enumerate(header_lines):
        if line.strip():
            story.append(Paragraph(line, header_style))

        if index in (3, 4):
            story.append(Spacer(1, 10))

    story.append(Spacer(1, 14))

    # Greeting
    story.append(
        Paragraph(
            cover_letter.greeting,
            greeting_style,
        )
    )

    # Opening
    story.append(
        Paragraph(
            cover_letter.opening,
            body_style,
        )
    )

    # Body paragraphs
    for paragraph in cover_letter.body:
        story.append(
            Paragraph(
                paragraph,
                body_style,
            )
        )

    # Closing
    story.append(
        Paragraph(
            cover_letter.closing,
            closing_style,
        )
    )

    # Sign off
    story.append(Spacer(1, 10))

    sign_off = cover_letter.sign_off.strip()
    candidate_name = candidate.name.strip()

    if sign_off.casefold().endswith(candidate_name.casefold()):
        sign_off = sign_off[: -len(candidate_name)].rstrip()

    story.append(
        Paragraph(
            sign_off,
            signoff_style,
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            candidate_name,
            signoff_style,
        )
    )

    document.build(story)