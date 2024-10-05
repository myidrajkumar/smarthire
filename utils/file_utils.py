"""Utilities to handle files"""

import pathlib

import docx
import pypdf as pdf


def get_file_content(file_path):
    """Retrieving file content based on type"""

    if file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        text = ""

        for para in doc.paragraphs:
            text += para.text
        return text
    if file_path.endswith(".pdf"):
        reader = pdf.PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += str(page.extract_text())
        return text

    print(f"ERROR: Unsupported file type: {file_path}")
    return None


def get_file_content_binary(file_path):
    """Retrieving file content based on type"""

    with open(file_path, "rb") as f:
        binary_data = f.read()

    return binary_data


def save_file_content(file_path, file_data):
    """Storing files"""

    pathlib.Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "wb") as file:
        file.write(file_data)
