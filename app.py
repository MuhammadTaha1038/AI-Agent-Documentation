import streamlit as st

from agent import (
    analyze_requirement,
    analyze_document
)

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="23-SE-100",
    page_icon="🤖",
    layout="wide"
)

# =====================================
# Header
# =====================================

st.title(" AI Software Requirements Analysis Agent ")

st.markdown(
    """
This AI Agent analyzes software requirements and automatically:

- Extracts Functional Requirements (FRs)

- Extracts Non-Functional Requirements (NFRs)

- Generates User Stories

- Detects Missing Requirements

- Detects Ambiguous Requirements

- Evaluates Requirement Quality

- Supports TXT, PDF and DOCX Requirement Documents
"""
)

st.divider()

# =====================================
# Input Method Selection
# =====================================

input_type = st.radio(
    "Choose Input Method",
    [
        "Text Requirement",
        "Requirement Document"
    ]
)

response = None

# =====================================
# Text Input
# =====================================

if input_type == "Text Requirement":

    st.subheader("Enter Software Requirement")

    requirement = st.text_area(
        "Describe your software idea or client requirement:",
        height=250,
        placeholder="""
Example:

I want a university management system where students
can register courses, teachers upload marks,
and administrators manage users.
"""
    )

    if st.button("Analyze Requirement "):

        if requirement.strip() == "":

            st.warning(
                "Please enter a software requirement."
            )

        else:

            with st.spinner(
                "Analyzing requirement..."
            ):

                response = analyze_requirement(
                    requirement
                )

# =====================================
# Document Upload
# =====================================

else:

    st.subheader("Upload Requirement Document")

    uploaded_file = st.file_uploader(
        "Upload TXT, DOCX or PDF",
        type=["txt", "docx", "pdf"]
    )

    if st.button("Analyze Document "):

        if uploaded_file is None:

            st.warning(
                "Please upload a document."
            )

        else:

            with st.spinner(
                "Analyzing document..."
            ):

                response = analyze_document(
                    uploaded_file
                )

# =====================================
# Results Section
# =====================================

if response:

    st.success(
        "Requirement Analysis Completed!"
    )

    st.divider()

    st.subheader(
        "Analysis Report"
    )

    st.markdown(response)

    st.download_button(
        label="  Download Report",
        data=response,
        file_name="Requirement_Analysis_Report.txt",
        mime="text/plain"
    )

# =====================================
# Footer
# =====================================

st.divider()

st.caption(
    """
AI Software Requirements Analysis Agent

Artificial Intelligence Semester Project (sorry for previous viva performance )

Features:
Requirement Extraction • FR/NFR Classification •
Requirement Quality Analysis • Document Analysis
"""
)