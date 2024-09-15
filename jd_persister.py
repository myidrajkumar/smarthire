"""Save the JD"""

import pathlib
import pypandoc
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from db.connect import get_business_units

DOCS_FOLDER = "docs"


def save_jd_and_retrieve(llm_response, job_title, bu_id):
    """Persist the JD into folder"""

    bu_name = get_business_units(bu_id)[0].get("name")
    folder_path = "".join([DOCS_FOLDER, "/", bu_name])

    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)

    save_jd_txt(llm_response, file_name=job_title, folder_path=folder_path)
    save_jd_doc(llm_response, file_name=job_title, folder_path=folder_path)
    # save_jd_pdf(llm_response, file_name=job_title, folder_path=folder_path)
    return job_title


def save_jd_doc(llm_response, file_name, folder_path):
    """Persist the JD as Document"""
    bullet_style = "List Bullet"

    doc = Document()
    page_title = doc.add_heading(
        file_name,
        level=0,
    )
    page_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading("Job Description:", level=1)
    doc.add_paragraph(llm_response.get("Description"))

    doc.add_heading("Responsibilities:", level=1)
    for responsibility in llm_response.get("Responsibilities"):
        doc.add_paragraph(responsibility, bullet_style)

    doc.add_heading("Skills:", level=1)
    for responsibility in llm_response.get("Skills"):
        doc.add_paragraph(responsibility, bullet_style)

    doc.add_heading("Experience:", level=1)
    for responsibility in llm_response.get("Experience"):
        doc.add_paragraph(responsibility, bullet_style)

    # for _ in range(2):
    #     doc.add_paragraph()

    # paragraph = doc.add_paragraph(llm_response.get("ClosingStatement"))
    # paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.save(f"{folder_path}/{file_name}.docx")
    return f"{file_name}.docx"


def save_jd_pdf(llm_response, file_name, folder_path):
    """Persist the JD as PDF"""
    c = canvas.Canvas(f"{folder_path}/{file_name}.pdf", pagesize=A4)
    width, height = A4

    # Set title of the document
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2.0, height - 100, f"{file_name}")

    # Description
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 150, f"Description:")

    c.setFont("Helvetica-Oblique", 12)
    y_position = height - 170
    wrapped_lines = wrap_text(c, llm_response.get("Description"), width - 150)
    c.drawString(100, y_position, "")
    for line in wrapped_lines:
        c.drawString(115, y_position, line)  # Indent text after bullet
        y_position -= 15  # Move down for the next line

    # Responsibilities Header
    y_position -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y_position, "Responsibilities:")

    # Responsibilities List
    c.setFont("Helvetica-Oblique", 12)
    bullet = "•"
    responsibilities = llm_response.get("Responsibilities")
    for idx, responsibility in enumerate(responsibilities, 1):
        c.drawString(120, y_position - (idx * 20), f"{bullet} {responsibility}")

    # Skills Header
    y_position = y_position - (len(responsibilities) * 20) - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y_position, "Skills:")

    # Skills List
    c.setFont("Helvetica-Oblique", 12)
    skills = llm_response.get("Skills")
    for idx, skill in enumerate(skills, 1):
        c.drawString(120, y_position - (idx * 20), f"{bullet} {skill}")

    # Experience Header
    y_position = y_position - (len(skills) * 20) - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y_position, "Experience:")

    # Experience List
    c.setFont("Helvetica-Oblique", 12)
    experiences = llm_response.get("Experience")
    for idx, ex in enumerate(experiences, 1):
        c.drawString(120, y_position - (idx * 20), f"{bullet} {ex}")

    # Save the PDF
    c.showPage()
    c.save()
    return f"{file_name}.pdf"


def save_jd_txt(llm_response, file_name, folder_path):
    """Persist the JD as TXT"""
    save_jd_doc(llm_response, file_name, folder_path)
    pypandoc.convert_file(
        f"{folder_path}/{file_name}.docx",
        "plain",
        outputfile=f"{folder_path}/{file_name}.txt",
    )
    return f"{file_name}.txt"


# Helper function to wrap text within the specified width
def wrap_text(c, text, max_width):
    lines = []
    words = text.split(" ")
    current_line = ""
    for word in words:
        if c.stringWidth(current_line + word, "Helvetica", 12) < max_width:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines
