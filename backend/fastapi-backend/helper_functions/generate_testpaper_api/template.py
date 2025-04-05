from langchain_core.prompts import ChatPromptTemplate
# json_example = """```json
# {{
#   "MCQ": [
#     {{"question": "What is the unit of current?", "options": ["Ampere", "Volt", "Ohm", "Watt"], "answer": "Ampere"}},
#     ...
#   ],
#   "short_answer": [
#     {{"question": "Explain the concept of electric circuit."}},
#     ...
#   ]
# }}
# ```"""
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
Also, you must always generate questions in json format 
Use the following context to generate the questions:
{context}
            """
        ),
    ]
)
