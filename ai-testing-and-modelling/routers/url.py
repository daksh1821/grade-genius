from fastapi import(
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
from logger import(
    logger
)
from helper_functions.timetable_api.crop_to_table import auto_crop_table
import shutil
from pathlib import Path
UPLOAD_DIR=Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
router=APIRouter()
@router.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
@router.post("/api/timetable/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    API endpoint to upload an image and automatically crop the timetable region.

    Args:
        file (UploadFile): Image file uploaded by the frontend.

    Returns:
        JSON response containing the path of the cropped image and its size.
    """
    try:
        # Save the uploaded file to disk
        image_path = UPLOAD_DIR / file.filename
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        output_path = UPLOAD_DIR / f"cropped_{file.filename}"
        cropped_path = auto_crop_table(str(image_path), str(output_path))

        return JSONResponse({
            "message": "Timetable image uploaded and cropped successfully!",
            "cropped_image_path": str(cropped_path)
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")