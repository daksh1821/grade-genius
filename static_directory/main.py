from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict
import json
import os
import uvicorn
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class AnswerSubmission(BaseModel):
    answers: Dict[str, str]
@app.get("/questions")
async def get_questions():
    return {
  "questions": [
    {
      "id": 1,
      "type": "multiple_choice",
      "question": "Which of the following algorithms is most suitable for solving a classification problem?",
      "options": ["Linear Regression", "Logistic Regression", "K-Means", "PCA"],
      "answer": "Logistic Regression"
    },
    {
      "id": 2,
      "type": "multiple_choice",
      "question": "What is the purpose of the activation function in a neural network?",
      "options": [
        "To initialize weights",
        "To reduce overfitting",
        "To introduce non-linearity",
        "To normalize data"
      ],
      "answer": "To introduce non-linearity"
    },
    {
      "id": 3,
      "type": "multiple_choice",
      "question": "Which of the following evaluation metrics is most appropriate for an imbalanced classification problem?",
      "options": ["Accuracy", "MSE", "F1 Score", "R-squared"],
      "answer": "F1 Score"
    },
    {
      "id": 4,
      "type": "numerical",
      "question": "A linear regression model predicts the value of y using the equation y = 2x + 3. What is the predicted value of y when x = 5?",
      "answer": "13"
    }
  ]
}

@app.post("/submit")
async def submit_answers(submission: AnswerSubmission):
    os.makedirs("submissions", exist_ok=True)
    with open("submissions/saved_answers.json", "w") as f:
        json.dump(submission.dict(), f, indent=2)
    return {"status": "success", "message": "Answers saved"}
@app.post("/upload-snapshot")
async def upload_snapshot(image: UploadFile = File(...)):
    contents = await image.read()
    with open(f"submissions/{image.filename}", "wb") as f:
        f.write(contents)
    return {"status": "success", "filename": image.filename}
if __name__=='__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


# from fastapi import FastAPI, Form, Request, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from typing import List, Dict
# import json
# import os
# import datetime
# import base64

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust for production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class AnswerSubmission(BaseModel):
#     answers: Dict[str, str]

# class EventLog(BaseModel):
#     event: str
#     timestamp: str

# class AudioLog(BaseModel):
#     level: str
#     timestamp: str

# class SnapshotBase64(BaseModel):
#     image: str  # base64 string
#     timestamp: str

# EXAM = {
#     "title": "Midterm Examination - Mathematics",
#     "instructions": "Answer all questions. Each question carries equal marks.",
#     "questions": [
#         {"id": 1, "type": "short_answer", "question": "Define a function in mathematics with an example."},
#         {"id": 2, "type": "multiple_choice", "question": "Which of the following is a prime number?", "options": ["4", "6", "9", "11"]},
#         {"id": 3, "type": "long_answer", "question": "Explain the concept of limits in calculus."}
#     ]
# }

# @app.get("/exam")
# def get_exam():
#     return EXAM

# @app.post("/submit")
# async def submit_answers(submission: AnswerSubmission):
#     os.makedirs("submissions", exist_ok=True)
#     with open("submissions/saved_answers.json", "w") as f:
#         json.dump(submission.dict(), f, indent=2)
#     return {"status": "success", "message": "Answers saved"}

# @app.post("/snapshot")
# async def receive_snapshot(data: SnapshotBase64):
#     os.makedirs("photos", exist_ok=True)
#     img_data = base64.b64decode(data.image.split(",")[1])
#     filename = f"photos/snapshot_{data.timestamp}.png"
#     with open(filename, "wb") as f:
#         f.write(img_data)
#     return {"status": "success", "message": f"Snapshot saved at {filename}"}

# @app.post("/log-event")
# async def log_tab_event(event: EventLog):
#     os.makedirs("cheating", exist_ok=True)
#     with open("cheating/tab_log.json", "a") as f:
#         json.dump(event.dict(), f)
#         f.write("\n")
#     return {"status": "logged"}

# @app.post("/log-audio")
# async def log_audio_event(audio: AudioLog):
#     os.makedirs("cheating", exist_ok=True)
#     with open("cheating/audio_log.json", "a") as f:
#         json.dump(audio.dict(), f)
#         f.write("\n")
#     return {"status": "audio event logged"}
