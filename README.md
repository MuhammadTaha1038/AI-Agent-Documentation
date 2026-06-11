#  AI Software Requirements Analysis Agent

An Artificial Intelligence based Software Requirements Engineering Assistant that automatically analyzes software requirements and generates a structured Software Requirement Specification (SRS).

This project was developed as a semester project for the **Artificial Intelligence** course.

---

#  Project Overview

Software requirements are often written in informal language and may contain missing, incomplete, or ambiguous information.

This system uses a Large Language Model (LLM) to analyze software requirements provided by users and automatically generate:

* Project Overview
* Actors and Stakeholders
* Functional Requirements (FRs)
* Non-Functional Requirements (NFRs)
* User Stories
* Missing Requirements
* Ambiguous Requirements
* Requirement Quality Assessment

The system supports both direct text input and uploaded requirement documents.

---

#  Features

### Requirement Analysis

* Extract Functional Requirements
* Extract Non-Functional Requirements
* Generate User Stories
* Identify Stakeholders and Actors

### Requirement Quality Evaluation

* Detect Missing Requirements
* Detect Ambiguous Requirements
* Evaluate Requirement Completeness

### Document Processing

Supports:

* TXT Files
* DOCX Files
* PDF Files

### Input Validation

Rejects non-software-related inputs and requests.

---

#  System Architecture

```text
User
 │
 ▼
Streamlit Web Interface
 │
 ├── Text Input
 │
 └── Document Upload
        │
        ▼
Document Processing Module
        │
        ▼
Prompt Engineering Module
        │
        ▼
AI Requirement Analysis Agent
        │
 ┌──────┼─────────┬──────────┐
 ▼      ▼         ▼          ▼
FRs    NFRs   User Stories  Actors
 │
 ▼
Missing Requirements
 │
 ▼
Ambiguous Requirements
 │
 ▼
Quality Assessment
 │
 ▼
Analysis Report
```

---

#  AI Methodology

The project follows an Agent-Based AI approach.

### Step 1 – Input Collection

User enters:

* Requirement text

OR

* Requirement document

### Step 2 – Document Processing

The system extracts text from uploaded files.

### Step 3 – Prompt Engineering

Requirements are transformed into a structured AI prompt.

### Step 4 – AI Analysis

The language model performs:

* Requirement Understanding
* Requirement Extraction
* Requirement Evaluation

### Step 5 – Report Generation

The system generates a structured requirement analysis report.

---

#  Technologies Used

| Technology                  | Purpose                         |
| --------------------------- | ------------------------------- |
| Python                      | Backend Development             |
| Streamlit                   | User Interface                  |
| OpenRouter API              | AI Model Access                 |
| NVIDIA Nemotron 3 Nano Omni | Requirement Analysis            |
| PyPDF2                      | PDF Processing                  |
| python-docx                 | DOCX Processing                 |
| python-dotenv               | Environment Variable Management |

---

#  Project Structure

```text
project/
│
├── app.py
│
├── agent.py
│
├── prompts.py
│
├── requirements.txt
│
├── .env
│
└── README.md
```

---

#   Installation

## 1. Clone Repository

```bash
git clone https://github.com/MuhammadTaha1038/AI-Agent-Documentation.git

cd ai-requirements-agent
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

#  Environment Variables

Create a `.env` file in the project root.

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

#   Running the Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

#   Example Input

```text
I want an online food delivery system where users can create accounts, browse restaurants, order food, pay online, and track deliveries.
Restaurants should manage menus and delivery riders should update order status.
```

---

#   Example Output

The AI generates:

* Project Overview
* Actors
* Functional Requirements
* Non-Functional Requirements
* User Stories
* Missing Requirements
* Ambiguous Requirements
* Requirement Quality Assessment

---

#   Future Enhancements

Possible future improvements include:

* UML Diagram Generation
* Use Case Diagram Generation
* ER Diagram Generation
* Requirement Prioritization
* Risk Analysis
* OCR Support for Images
* Export to PDF/DOCX
* Multi-Agent Architecture

---

#   Academic Context

This project was developed as part of the **Artificial Intelligence** course and demonstrates the application of Large Language Models (LLMs) in Software Requirements Engineering.

---

#   Author

Semester Project

Artificial Intelligence Course

Department of Software Engineering

```
Name: Muhammad Taha

Reg no: 23-SE-100
```
