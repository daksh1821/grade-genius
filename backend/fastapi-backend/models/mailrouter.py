from pydantic import BaseModel
class EmailRequest(BaseModel):
    to:str
    subject:str
    body:str
