from pydantic import BaseModel,EmailStr
from typing import List
# class EmailRequest(BaseModel):
#     to:str
#     subject:str
#     body:str
class EmailRequest(BaseModel):
    to: List[EmailStr]               # List of emails
    student_id: List[str]           # List of student IDs
    user_id: str                    # Single user ID
    class_id: str     
