import uvicorn
from config import settings
from fastapi import FastAPI

from src.api.router import api_router

app = FastAPI(
    title=settings.TITLE,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    debug=settings.debug,
)

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
