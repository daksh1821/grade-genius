from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert exam paper generator for academic institutions. Your task is to create well-structured, relevant, and clear question papers based strictly on the format provided by the user.",
        ),
        (
            "human",
            """
I will be passing context, which is extracted content from a pdf file.
Generate questions based on the following criteria:

- Class Level: {class_level}
- Chapter Background: {chapter_background}
- Question Requirements: {question_types}

Use the following context to generate the questions:
{context}
            """
        ),
    ]
)
