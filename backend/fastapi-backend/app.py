from fastapi import FastAPI,File,UploadFile
from pydantic import BaseModel
from typing import Optional
from PIL import Image
import numpy as np
import io
app=FastAPI()
class Item(BaseModel):
    name:str
    description: Optional[str]=None
    price:float
    tax:Optional[float]=None
@app.get("/")
def read_root():
    return {"message":"Hello from API"}
@app.get("/items/{item_id}")
def read_item(item_id:int,q:str=None):
    return {"item_id":item_id,"query":q}
@app.post("/upload-image/")
def upload_image(file:UploadFile=File(...)):
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents))
    image_array = np.array(image)
    return {"filename": file.filename, "image_shape": image_array.shape}
