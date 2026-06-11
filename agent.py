from openai import OpenAI
from dotenv import load_dotenv
from prompts import create_requirement_prompt

import os
import docx
import PyPDF2

# ==========================================
# Configuration
# ==========================================

load_dotenv()

MODEL_NAME = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ==========================================
# Token Optimization
# ==========================================

def truncate_text(text, max_chars=5000):
    """
    Prevent huge documents from consuming
    excessive tokens.
    """

    if not text:
        return ""

    if len(text) <= max_chars:
        return text

    return text[:max_chars]


# ==========================================
# TXT Reader
# ==========================================

def read_txt(file):

    return file.read().decode("utf-8")


# ==========================================
# DOCX Reader
# ==========================================

def read_docx(file):

    document = docx.Document(file)

    text = []

    for para in document.paragraphs:

        if para.text.strip():
            text.append(para.text)

    return "\n".join(text)


# ==========================================
# PDF Reader
# ==========================================

def read_pdf(file):

    reader = PyPDF2.PdfReader(file)

    text = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


# ==========================================
# Document Text Extraction
# ==========================================

def extract_document_text(uploaded_file):

    filename = uploaded_file.name.lower()

    if filename.endswith(".txt"):
        return read_txt(uploaded_file)

    elif filename.endswith(".docx"):
        return read_docx(uploaded_file)

    elif filename.endswith(".pdf"):
        return read_pdf(uploaded_file)

    raise Exception(
        "Unsupported file format. Upload TXT, DOCX, or PDF."
    )


# ==========================================
# Main Requirement Analysis Agent
# ==========================================

def analyze_requirement(requirement_text):

    try:

        requirement_text = truncate_text(
            requirement_text
        )

        prompt = create_requirement_prompt(
            requirement_text
        )

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        # Safety check
        if (
            not response.choices
            or response.choices[0].message is None
        ):
            return """
# Error

Model returned an empty response.
Please try again.
"""

        content = response.choices[0].message.content

        if not content:
            return """
# Error

Model returned no content.
Please try again.
"""

        return content

    except Exception as e:

        return f"""
# Error

{str(e)}
"""


# ==========================================
# Document Analysis Agent
# ==========================================

def analyze_document(uploaded_file):

    try:

        document_text = extract_document_text(
            uploaded_file
        )

        if not document_text.strip():

            return """
# Error

No readable text was found in the document.
"""

        return analyze_requirement(
            document_text
        )

    except Exception as e:

        return f"""
# Error

{str(e)}
"""
 