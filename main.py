import orjson
import uvicorn

from typing import Any
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.db.models import *
from app.core.config import get_settings
from app.api.routers import api_router

settings = get_settings()

origins = ['*']

class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)


app = FastAPI(title=settings.PROJECT_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(router=api_router, prefix='/api')

app.mount("/api/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=settings.APP_PORT, workers=settings.APP_WORKERS, reload=True)
    