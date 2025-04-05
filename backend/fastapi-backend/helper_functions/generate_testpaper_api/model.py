from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from helper_functions.generate_testpaper_api.template import prompt
def load_model():
    llm=ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-latest",
        temperature=0.85,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )
    return llm
def handle_user_conversations(number_of_questions,context):
    # probably
    llm=load_model()
    chain=prompt|llm
    output=chain.invoke(
        {
            "number_of_questions":number_of_questions,
            "context":
            context
        }
    )
    return output
