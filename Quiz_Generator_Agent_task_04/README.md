# PDF AI Agent: Summarizer & Quiz Generator

This project provides a Streamlit-based web application that allows you to upload PDF documents, extract their text, and then automatically generate a summary, key points, study questions, and a comprehensive quiz (multiple-choice and short-answer questions) using a Large Language Model (LLM).

## Features

-   **PDF Text Extraction:** Utilizes `pypdf` to accurately extract text content from uploaded PDF files.
-   **PDF Summarization:** Generates a concise summary (5-7 lines) and 5 key points from the PDF content.
-   **Study Question Generator:** Creates 3 relevant study questions based on the document's content.
-   **Quiz Generator:** Produces:
    -   5 Multiple-Choice Questions (A-D options with correct answers).
    -   3 Short-Answer Questions.
    -   All quiz output is formatted in clean JSON.
-   **Interactive Streamlit UI:** A user-friendly web interface for uploading PDFs and viewing the generated outputs.

## Folder Structure

```
project/
│── agent.py
│── streamlit_app.py
│── requirements.txt
│── README.md
```

-   `agent.py`: Contains the core logic for PDF text extraction, summarization, and quiz generation, interacting with an LLM.
-   `streamlit_app.py`: Implements the Streamlit user interface for the application.
-   `requirements.txt`: Lists all necessary Python dependencies.
-   `README.md`: This file, providing project overview and instructions.

## Setup Instructions

### Prerequisites

Ensure you have Python 3.8+ installed on your system.

### 1. Clone the repository (if applicable)

```bash
# If you are setting this up as a new project, you can skip this step.
# Otherwise, clone the repository:
# git clone <repository-url>
# cd <repository-name>/project
```

### 2. Navigate to the project directory

If you cloned the repository, or extracted the files:

```bash
cd project
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure your Large Language Model (LLM)

This project is designed to work with an LLM (e.g., Google Gemini). The `agent.py` currently includes a mock LLM for demonstration. To use a real LLM, you will need to:

1.  **Obtain an API Key:** Get an API key for your chosen LLM (e.g., a Google Gemini API Key).
2.  **Integrate the LLM:**
    *   In `agent.py`, uncomment and modify the LLM initialization in the `PDFAgent.__init__` method. Replace `openagents.llm.Gemini` with the actual LLM client library you are using and pass your API key. For example:
        ```python
        # In agent.py
        # from openagents.llm import Gemini # or your actual LLM client
        # self.llm = Gemini(api_key="YOUR_API_KEY") # Replace with your API key or environment variable
        ```
    *   Alternatively, you can pass the LLM instance directly from `streamlit_app.py` to `PDFAgent`. Ensure your API key is handled securely (e.g., via environment variables or Streamlit secrets).

## How to Run

Once the setup is complete and your LLM is configured:

```bash
streamlit run streamlit_app.py
```

This command will start the Streamlit application, and it will open in your default web browser.

## Usage

1.  Open the application in your web browser.
2.  Use the "Upload your PDF document" button to select a PDF file.
3.  The application will process the PDF, extract text, and then display the generated summary, key points, study questions, and the complete quiz.
4.  The quiz results will include multiple-choice questions with options and answers, as well as short-answer questions.
