from fastapi import (
    APIRouter,
    status,
    HTTPException,
    File,
    UploadFile
)
from fastapi.responses import (
    RedirectResponse
)
import json
import asyncio
import fitz
import numpy as np
from utils.logger import logger
from helper_functions.timetable_api.crop_to_table import auto_crop_table
from helper_functions.timetable_api.ocr_functionality import process_cropped_image
from helper_functions.generate_testpaper_api.model import handle_user_conversations
import uuid
import cv2
import os
from models.question_generate_model import QuestionGenerationRequest
PDF_STORAGE_DIR="uploaded_pdfs"
os.makedirs(PDF_STORAGE_DIR,exist_ok=True)
router = APIRouter()

# import aiofiles
# from pathlib import Path
# from uuid import uuid4

# UPLOAD_DIR = Path("uploads") # Path /uploads/
# UPLOAD_DIR.mkdir(exist_ok=True)

@router.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@router.post("/api/timetable/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image and automatically crop the timetable region.

    Returns:
        JSON containing the path of the cropped image and its dimensions.
    """
    try:
        # Generate a unique filename to avoid clashes
        # file_extension = Path(file.filename).suffix
        # unique_filename = f"{uuid4().hex}{file_extension}"
        # image_path = UPLOAD_DIR / unique_filename

        # # Save file asynchronously
        # async with aiofiles.open(image_path, "wb") as out_file:
        #     content = await file.read()
        #     await out_file.write(content)

        content = await file.read()
        nparr=np.frombuffer(content,np.uint8)
        img=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        # output_path = UPLOAD_DIR / f"cropped_{unique_filename}"
        # cropped_path = auto_crop_table(str(image_path), str(output_path))

        # if cropped_path is None:
        #     logger.error(f"Cropping failed for {image_path}")
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         detail="An error occurred while cropping the image."
        #     )
        if img is None:
            logger.error(f"Failed to decode image from uploaded file: {file.filename}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image format."
            )
        logger.info(f"Image {file.filename} received and decoded successfully.")

        cropped_img = auto_crop_table(img)

        # OCR processing on the cropped image
        return process_cropped_image(cropped_img)

    except HTTPException as he:
        raise he  # already a well-formed HTTP error

    except Exception as e:
        logger.exception("Unexpected error during upload and crop")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

@router.post("/api/upload-pdf")
async def upload_pdf(pdf_file:UploadFile=File(...)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(PDF_STORAGE_DIR, f"{file_id}.pdf")


    with open(file_path, "wb") as f:
        f.write(await pdf_file.read())

    return {"file_id": file_id, "message": "PDF uploaded successfully"}
@router.post("/api/generate-questions")
async def generate_questions(request: QuestionGenerationRequest):
    file_path = os.path.join(PDF_STORAGE_DIR, f"{request.file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Please try uploading the pdf again")
    def extract_text():
        text = ""
        with fitz.open(file_path) as doc:
            for page_num in request.selected_pages:
                if 0 <= page_num < len(doc):
                    text += doc[page_num].get_text()
        return text
    logger.info(f"Extracting text from pages: {request.selected_pages}")
    text=await asyncio.to_thread(extract_text)
    logger.info("Text extraction completed.")
    output=handle_user_conversations(
        question_types=request.question_types,
        context=text,
        class_level=request.class_level,
        chapter_background=request.chapter_background
    )
    try:
        raw = output.content

        # Step 1: Convert escaped characters into proper string (e.g., "\n" to actual newline)
        raw = raw.encode('utf-8').decode('unicode_escape')

        # Step 2: Remove markdown syntax like ```json ... ```
        cleaned = raw.strip().replace("```json", "").replace("```", "").strip()

        # Step 3: Now it's safe to parse as JSON
        parsed = json.loads(cleaned)

        return parsed
    except json.JSONDecodeError as e:
        return {"error":"Json Decode Failed","details":str(e)}

    # return {
    #     "extracted_text_preview": text[:500],  # Just to test
    #     "question_types": request.question_types,
    #     "class_level": request.class_level,
    #     "chapter_background": request.chapter_background
    # }
    # this text along with input stuff will be passed to the llm