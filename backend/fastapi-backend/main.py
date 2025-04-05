from contextlib import asynccontextmanager # <-- Import this
from fastapi import (
    FastAPI,
    File,
    UploadFile
)
from fastapi.middleware.cors import CORSMiddleware
from utils.logger import logger
from routers import url
import uvicorn 
@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("App starting up...")
    
    print("Simulating database pool start")

    logger.info("Startup complete. Application is ready.")

    yield 

    
    logger.info("App shutting down...")
   
    print("Simulating database pool closing")

    logger.info("Shutdown complete.")


app = FastAPI(lifespan=lifespan)

# only for development purposes
app.add_middleware(
    CORSMiddleware,
    # will be changed to id of website when deploue
    allow_origins=["*"],
    allow_credentials=True,
    # will be changed to GET, POST
    allow_methods=["*"],
    # will be changed to middleware headersthat are send in request
    allow_headers=["*"],
)




app.include_router(url.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)