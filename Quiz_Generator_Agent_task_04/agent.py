import pypdf
import json
# Assuming openagents provides an LLM interface
# from openagents.llm import Gemini # Placeholder for actual import

class PDFAgent:
    def __init__(self, llm_model=None):
        """
        Initializes the PDF Agent with an LLM model.
        The llm_model should be an instance of a class that can generate responses,
        e.g., from openagents.llm.Gemini.
        """
        if llm_model is None:
            # Placeholder for actual LLM initialization
            # In a real scenario, you would initialize your Gemini model here.
            # For example:
            # self.llm = Gemini(api_key="YOUR_API_KEY")
            # For now, we'll use a mock or raise an error if generation is attempted.
            print("Warning: LLM model not provided. Summarization and quiz generation will be mocked.")
            self.llm = self._mock_llm()
        else:
            self.llm = llm_model

    def _mock_llm(self):
        """
        A mock LLM for testing purposes when a real LLM is not provided.
        """
        class MockLLM:
            def generate(self, prompt, **kwargs):
                if "summary" in prompt.lower():
                    return "Mock Summary: This PDF discusses various topics related to mock data generation and its applications. It highlights the importance of placeholders in development workflows. The document also touches upon the challenges of creating realistic mock content and suggests best practices for maintaining data integrity. Furthermore, it explores the integration of mock data with modern web frameworks. Finally, it provides insights into the future of data simulation technologies."
                elif "key points" in prompt.lower():
                    return "- Mock Key Point 1: Importance of mock data\n- Mock Key Point 2: Challenges in realistic data\n- Mock Key Point 3: Best practices for integrity\n- Mock Key Point 4: Integration with web frameworks\n- Mock Key Point 5: Future of data simulation"
                elif "study questions" in prompt.lower():
                    return "1. What is the primary purpose of mock data mentioned in the PDF?\n2. List two challenges in generating realistic mock content.\n3. How does the PDF suggest integrating mock data with web frameworks?"
                elif "multiple choice" in prompt.lower():
                    return json.dumps({
                        "mcqs": [
                            {"question": "What is the capital of France?", "options": ["A. Berlin", "B. Madrid", "C. Paris", "D. Rome"], "answer": "C"},
                            {"question": "Which planet is known as the Red Planet?", "options": ["A. Earth", "B. Mars", "C. Jupiter", "D. Venus"], "answer": "B"},
                            {"question": "What is 2 + 2?", "options": ["A. 3", "B. 4", "C. 5", "D. 6"], "answer": "B"},
                            {"question": "Who wrote 'Romeo and Juliet'?", "options": ["A. Charles Dickens", "B. William Shakespeare", "C. Jane Austen", "D. Mark Twain"], "answer": "B"},
                            {"question": "What is the largest ocean on Earth?", "options": ["A. Atlantic", "B. Indian", "C. Arctic", "D. Pacific"], "answer": "D"},
                        ]
                    })
                elif "short answer" in prompt.lower():
                    return json.dumps({
                        "short_answer_questions": [
                            {"question": "What is photosynthesis?"},
                            {"question": "Explain the theory of relativity."},
                            {"question": "Name three types of clouds."}
                        ]
                    })
                return "Mock LLM Response"
        return MockLLM()

    def extract_text_from_pdf(self, pdf_file_path: str) -> str:
        """
        Extracts all text from a PDF file.

        Args:
            pdf_file_path: The path to the PDF file.

        Returns:
            A string containing all extracted text.
        """
        try:
            reader = pypdf.PdfReader(pdf_file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def summarize_pdf(self, text: str):
        """
        Generates a summary, key points, and study questions from the given text.

        Args:
            text: The full text extracted from the PDF.

        Returns:
            A dictionary containing the short_summary, key_points, and study_questions.
        """
        if not text:
            return {
                "short_summary": "No text provided for summarization.",
                "key_points": [],
                "study_questions": []
            }

        try:
            # Generate short summary
            summary_prompt = f"Please provide a short summary (5-7 lines) of the following text:\n\n{text}"
            short_summary = self.llm.generate(summary_prompt)

            # Generate 5 key points
            key_points_prompt = f"From the following text, extract 5 key points:\n\n{text}"
            key_points_raw = self.llm.generate(key_points_prompt)
            key_points = [point.strip() for point in key_points_raw.split('\n') if point.strip()]

            # Generate 3 study questions
            study_questions_prompt = f"Based on the following text, generate 3 study questions:\n\n{text}"
            study_questions_raw = self.llm.generate(study_questions_prompt)
            study_questions = [q.strip() for q in study_questions_raw.split('\n') if q.strip()]

            return {
                "short_summary": short_summary,
                "key_points": key_points,
                "study_questions": study_questions
            }
        except Exception as e:
            print(f"Error during summarization: {e}")
            return {
                "short_summary": f"Error generating summary: {e}",
                "key_points": [],
                "study_questions": []
            }

    def generate_quiz(self, text: str):
        """
        Generates multiple-choice and short-answer questions from the given text.

        Args:
            text: The full text extracted from the PDF.

        Returns:
            A JSON string containing mcqs and short_answer_questions.
        """
        if not text:
            return json.dumps({
                "mcqs": [],
                "short_answer_questions": []
            })

        try:
            # Generate 5 MCQs
            mcq_prompt = f"""
            From the following text, generate 5 multiple-choice questions (A-D) with the correct answer indicated.
            Format the output as a JSON array of objects, each with "question", "options" (an array of strings), and "answer" (the letter A, B, C, or D).

            Example format:
            {{
                "mcqs": [
                    {{"question": "...", "options": ["A. ...", "B. ...", "C. ...", "D. ..."], "answer": "A"}},
                    ...
                ]
            }}

            Text:\n\n{text}
            """
            mcqs_json_str = self.llm.generate(mcq_prompt)
            # Assuming LLM returns a valid JSON string
            mcqs = json.loads(mcqs_json_str)

            # Generate 3 short-answer questions
            short_answer_prompt = f"""
            From the following text, generate 3 short-answer questions.
            Format the output as a JSON array of objects, each with a "question" key.

            Example format:
            {{
                "short_answer_questions": [
                    {{"question": "..."}},
                    ...
                ]
            }}

            Text:\n\n{text}
            """
            short_answer_json_str = self.llm.generate(short_answer_prompt)
            # Assuming LLM returns a valid JSON string
            short_answer_questions = json.loads(short_answer_json_str)

            return json.dumps({
                "mcqs": mcqs.get("mcqs", []),
                "short_answer_questions": short_answer_questions.get("short_answer_questions", [])
            }, indent=2)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from LLM response: {e}")
            return json.dumps({"error": f"Failed to decode JSON from LLM: {e}", "raw_mcq_response": mcqs_json_str, "raw_sa_response": short_answer_json_str})
        except Exception as e:
            print(f"Error during quiz generation: {e}")
            return json.dumps({"error": f"Failed to generate quiz: {e}"})

if __name__ == "__main__":
    # Example usage (for testing agent.py directly)
    # This part assumes you have a PDF file named 'sample.pdf' in the same directory
    # and a properly initialized LLM.

    # You would replace this with your actual LLM initialization
    # agent = PDFAgent(llm_model=Gemini(api_key="YOUR_API_KEY"))
    agent = PDFAgent() # Using mock LLM for direct testing

    # Create a dummy PDF for local testing if you don't have one
    # This part is commented out as it requires reportlab or similar,
    # which is not in our requirements.txt and would add complexity.
    # For actual testing, please ensure 'sample.pdf' exists or create one manually.
    # try:
    #     from reportlab.pdfgen import canvas
    #     from reportlab.lib.pagesizes import letter
    #     c = canvas.Canvas("sample.pdf", pagesize=letter)
    #     c.drawString(100, 750, "This is a sample PDF document.")
    #     c.drawString(100, 730, "It contains some text about various topics.")
    #     c.drawString(100, 710, "This is the third line of the sample PDF.")
    #     c.save()
    #     print("Created 'sample.pdf' for testing.")
    # except ImportError:
    #     print("reportlab not installed. Cannot create sample PDF. Please provide 'sample.pdf' manually for testing.")


    sample_pdf_path = "sample.pdf" # Make sure this file exists for local testing

    try:
        # For demonstration, let's create a dummy file to avoid FileNotFoundError
        # In a real scenario, the user would upload a PDF via Streamlit
        with open(sample_pdf_path, "w") as f:
            f.write("This is a dummy PDF content for testing purposes. It talks about AI, machine learning, and natural language processing. Key points include: data privacy, model interpretability, and ethical AI. Some study questions could be: What is AI? How does machine learning work? What are the ethical considerations in AI?")
        print(f"Dummy file '{sample_pdf_path}' created for testing `extract_text_from_pdf` locally.")

        extracted_text = agent.extract_text_from_pdf(sample_pdf_path)
        if extracted_text:
            print("\n--- Extracted Text ---")
            print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)

            print("\n--- Summarization ---")
            summary_results = agent.summarize_pdf(extracted_text)
            print("Short Summary:", summary_results["short_summary"])
            print("Key Points:", summary_results["key_points"])
            print("Study Questions:", summary_results["study_questions"])

            print("\n--- Quiz Generation ---")
            quiz_results = agent.generate_quiz(extracted_text)
            print(quiz_results)
        else:
            print("Could not extract text from PDF.")
            
        import os
        os.remove(sample_pdf_path) # Clean up the dummy file
        print(f"Dummy file '{sample_pdf_path}' removed.")

    except FileNotFoundError:
        print(f"Error: The file '{sample_pdf_path}' was not found. Please create it for local testing or ensure the path is correct.")
    except Exception as e:
        print(f"An unexpected error occurred during direct agent.py testing: {e}")
