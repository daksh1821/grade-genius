from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from helper_functions.generate_testpaper_api.template import prompt
from utils.logger import logger
def load_model():
    llm=ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-latest",
        temperature=0.85,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )
    return llm
def handle_user_conversations(question_types, context, class_level, chapter_background):
    logger.info("Loading model...")
    llm=load_model()
    chain=prompt|llm
    logger.info("Generating questions with the following parameters:")
    logger.info(f"Question Types: {question_types}")
    logger.info(f"Class Level: {class_level}")
    logger.info(f"Chapter Background: {chapter_background}")
    output = chain.invoke(
        {
            "question_types": question_types,
            "context": context,
            "class_level": class_level,
            "chapter_background": chapter_background,
        }
    )

    logger.info("Questions generated successfully.")
    return output
