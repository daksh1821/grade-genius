from fastapi import (
    APIRouter,
    Request,
    status,
    HTTPException,
    File,
    UploadFile
)
from fastapi.responses import (
    JSONResponse,
    RedirectResponse
)
import numpy as np
from logger import logger
from helper_functions.timetable_api.crop_to_table import auto_crop_table
from helper_functions.timetable_api.ocr_functionality import process_cropped_image
import cv2
# import aiofiles
# from pathlib import Path
# from uuid import uuid4

# UPLOAD_DIR = Path("uploads") # Path /uploads/
# UPLOAD_DIR.mkdir(exist_ok=True)

router = APIRouter()

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
