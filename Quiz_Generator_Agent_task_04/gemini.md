# Gemini Instructions — PDF Summarizer & Quiz Generator Agent
You are an AI agent builder using:
- OpenAgents SDK
- Context7 MCP server (already connected)
- Python
- Streamlit
- PyPDF
- Gemini CLI

Your job is to generate a complete working project that includes:
1. PDF Summarizer
2. Quiz Generator
3. Streamlit UI
4. Requirements file
5. README file
6. agent.py (logic)
7. streamlit_app.py (front-end)
8. Proper folder structure
9. Clean code that runs without modification

-------------------------
# 🎯 Project Requirements
## 1. PDF Summarizer
The agent must:
- Accept a PDF
- Extract text using PyPDF
- Generate:
  - Short summary (5–7 lines)
  - 5 key points
  - 3 study questions

## 2. Quiz Generator
The agent must:
- Read the full PDF (not the summary)
- Generate:
  - 5 MCQs (A–D) with correct answers
  - 3 short-answer questions
- Return quiz output in clean JSON format

-------------------------
# 📂 Folder Structure (create this)
project/
│── agent.py
│── streamlit_app.py
│── requirements.txt
│── README.md

-------------------------
# 🧠 Technical Rules
- Use Streamlit for UI
- Use PyPDF for PDF extraction
- Use OpenAgents SDK for agent structure
- Use Context7 MCP tools if needed
- Ensure JSON output for quiz
- Code must run locally with:
  streamlit run streamlit_app.py

-------------------------
# 📝 What to Output
When I run this instruction, output:

1. agent.py full code  
2. streamlit_app.py full code  
3. requirements.txt  
4. README.md  
5. Short explanation of how to run the project  

All files must be complete and production-ready.

-------------------------
# ✔ Additional Instructions
- Write clean, readable Python
- Add error handling
- Add comments
- Don’t use extra libraries
- Keep everything simple and stable