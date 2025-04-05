from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert exam paper generator for academic institutions. Your task is to create well-structured, relevant, and clear question papers based strictly on the format provided by the user",
        ),
        ("human",
        """
        I will be passing context, which is extracted content from a pdf file.
        You need to Generate {number_of_questions} MCQ's from the context.
        {context}
        """
        ),
    ]
)
