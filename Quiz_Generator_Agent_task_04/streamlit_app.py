import streamlit as st
import tempfile
import os
import json # Import json for pretty printing quiz output

from agent import PDFAgent # Assuming agent.py is in the same directory or accessible

def main():
    st.set_page_config(page_title="PDF AI Agent", layout="wide")
    st.title("📄 PDF Summarizer & Quiz Generator")
    st.markdown("""
        Upload a PDF, and this AI agent will generate a summary, key points,
        study questions, and a quiz (multiple-choice and short-answer questions).
    """)

    # Initialize the PDFAgent.
    # In a real application, you'd pass your actual LLM model here, e.g.:
    # from openagents.llm import Gemini
    # llm_instance = Gemini(api_key=st.secrets["GEMINI_API_KEY"]) # Assuming API key is in Streamlit secrets
    # agent = PDFAgent(llm_model=llm_instance)
    
    # For now, we use the mock LLM built into PDFAgent if no llm_model is passed.
    agent = PDFAgent()

    uploaded_file = st.file_uploader("Upload your PDF document", type=["pdf"])

    if uploaded_file is not None:
        with st.spinner("Processing PDF..."):
            # Save the uploaded PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_pdf_path = tmp_file.name

            try:
                # Extract text
                st.subheader("Extracting Text...")
                extracted_text = agent.extract_text_from_pdf(tmp_pdf_path)
                if not extracted_text:
                    st.error("Could not extract text from the PDF. The file might be scanned, corrupted, or empty.")
                    return

                # Summarization
                st.subheader("📝 Summary & Study Questions")
                summary_results = agent.summarize_pdf(extracted_text)
                st.write("---")
                st.markdown("**Short Summary:**")
                st.info(summary_results["short_summary"])

                st.markdown("**Key Points:**")
                for i, point in enumerate(summary_results["key_points"]):
                    st.write(f"- {point}")

                st.markdown("**Study Questions:**")
                for i, question in enumerate(summary_results["study_questions"]):
                    st.write(f"{i+1}. {question}")
                st.write("---")

                # Quiz Generation
                st.subheader("🧠 Quiz Time!")
                quiz_results_json = agent.generate_quiz(extracted_text)
                
                try:
                    quiz_data = json.loads(quiz_results_json)
                    
                    st.markdown("**Multiple Choice Questions:**")
                    if quiz_data.get("mcqs"):
                        for i, mcq in enumerate(quiz_data["mcqs"]):
                            st.markdown(f"**{i+1}. {mcq['question']}**")
                            for option in mcq['options']:
                                st.write(option)
                            st.markdown(f"**Correct Answer: {mcq['answer']}**")
                            st.write("") # Add a newline for spacing
                    else:
                        st.write("No multiple-choice questions generated.")

                    st.markdown("**Short Answer Questions:**")
                    if quiz_data.get("short_answer_questions"):
                        for i, saq in enumerate(quiz_data["short_answer_questions"]):
                            st.markdown(f"**{i+1}. {saq['question']}**")
                            st.write("") # Add a newline for spacing
                    else:
                        st.write("No short-answer questions generated.")

                except json.JSONDecodeError:
                    st.error("Failed to parse quiz results (invalid JSON format).")
                    st.code(quiz_results_json, language="json") # Show raw output for debugging
                except Exception as e:
                    st.error(f"An error occurred while displaying quiz results: {e}")
                    st.code(quiz_results_json, language="json") # Show raw output for debugging


            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
            finally:
                # Clean up the temporary file
                os.remove(tmp_pdf_path)

    else:
        st.info("Please upload a PDF file to get started!")

if __name__ == "__main__":
    main()
