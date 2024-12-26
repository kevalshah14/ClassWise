import os
import uvicorn
from fastapi import FastAPI
from app.config import db

# Import your routers
from app.controller.auth_controller import auth_router

# Import all your models here (ensure models are imported for table creation)
from app.model import models

def init_app():
    app = FastAPI(
        title="DeQueue",
        description="Say goodbye to waitlists, and hello to your seat.",
        version="0.1.0",
    )

    # Add the routers
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

    @app.on_event("startup")
    async def on_startup():
        await db.init()        # Initialize and create database if needed
        await db.create_all()  # Create tables if they don't exist

    @app.on_event("shutdown")
    async def on_shutdown():
        await db.close()

    return app

app = init_app()

def start():
    # Get settings from environment variables or use default values
    UVICORN_HOST = os.getenv("UVICORN_HOST", "127.0.0.1")
    UVICORN_PORT = int(os.getenv("UVICORN_PORT", "8000"))
    UVICORN_RELOAD = os.getenv("UVICORN_RELOAD", "True").lower() == "true"

    uvicorn.run(
        "app.main:app",
        host=UVICORN_HOST,
        port=UVICORN_PORT,
        reload=UVICORN_RELOAD,
    )

if __name__ == "__main__":
    start()
