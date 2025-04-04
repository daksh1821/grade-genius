from contextlib import asynccontextmanager # <-- Import this
from fastapi import (
    FastAPI,
    File,
    UploadFile
)
from fastapi.middleware.cors import CORSMiddleware
from logger import logger
from routers import url
import uvicorn # <-- Moved import here for clarity

# Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    logger.info("App starting up...")
    # --- Placeholder: Initialize database pool here ---
    print("Simulating database pool start")
    # --- End Placeholder ---
    logger.info("Startup complete. Application is ready.")

    yield # The application runs while yielded

    # Code to run on shutdown
    logger.info("App shutting down...")
    # --- Placeholder: Clean up database pool here (if required) ---
    print("Simulating database pool closing")
    # --- End Placeholder ---
    # Corrected typo: ingo -> info
    logger.info("Shutdown complete.")

# Pass the lifespan manager to the FastAPI app
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


# Remove the old @app.on_event("startup") function
# @app.on_event("startup")
# async def startup():
#     logger.info("App started")
#     # database pool start

# Remove the old @app.on_event("shutdown") function
# @app.on_event("shutdown")
# async def shutdown():
#     logger.ingo("app shutted down") # Typo was here
#     # database pool end (if requird)

app.include_router(url.router)

if __name__ == "__main__":
    # import uvicorn # Original position
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)