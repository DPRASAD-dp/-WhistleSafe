# gemini_processing.py

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os


# ==========================
# SETUP GEMINI
# ==========================
def setup_gemini():
    """
    Initialize Gemini directly using API key (no environment variables).
    """
    GEMINI_API_KEY = ""  # <-- your key here

    try:
        gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.0,
            google_api_key=GEMINI_API_KEY  # <-- pass key directly
        )
        return gemini_llm, "Gemini LLM set up successfully."
    except Exception as e:
        return None, f"Error setting up Gemini LLM: {str(e)}"


# ==========================
# PROCESS TEXT REPORT
# ==========================
def process_question_with_doc(question, gemini_llm):
    """
    Processes a crime report using Gemini.
    NO LLMChain — direct invocation (LangChain 1.x compatible)
    """
    try:
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template="""
You are a chatbot that reads a crime report written by a user.
Do NOT add any extra information.

Crime Report Provided:
{question}

Format EXACTLY like this:

Time of Crime: <Extracted time or Not Found>
Place of Crime: <Extracted place or Not Found>
Crime Details: <Short summary strictly using given info>

Do NOT add anything extra.
"""
        )

        # Format the prompt
        formatted_prompt = prompt_template.format(question=question)

        # Send prompt directly to Gemini
        response = gemini_llm.invoke(formatted_prompt)

        # Extract the text output
        output_text = response.content if hasattr(response, "content") else str(response)

        return output_text.strip()

    except Exception as e:
        return f"Error processing question: {str(e)}"


# Example run
if __name__ == "__main__":
    gemini, msg = setup_gemini()
    print(msg)

    if gemini:
        test = "Yesterday evening at 7 PM in Main Street, a man stole a bike."
        print(process_question_with_doc(test, gemini))
