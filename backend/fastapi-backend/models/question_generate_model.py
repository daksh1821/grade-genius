from pydantic import BaseModel, Field
from typing import List, Dict

class QuestionGenerationRequest(BaseModel):
    file_id: str = Field(..., example="9f839d8a-3e58-4b2c-9f25-f25c1234abcd", description="Unique ID of the uploaded PDF")
    selected_pages: List[int] = Field(..., example=[0, 1, 2], description="Pages to extract content from (0-indexed)")
    question_types: Dict[str, int] = Field(
        ..., 
        example={"MCQ": 3, "short_answer": 2},
        description="Types of questions to generate with their counts"
    )
    class_level: str = Field(..., example="Class 8", description="Academic level or grade")
    chapter_background: str = Field(
        ..., 
        example="This chapter explains the basics of electricity and electrical circuits.",
        description="Brief context to help LLM generate relevant questions"
    )
