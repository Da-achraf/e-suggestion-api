
import orjson
import uvicorn

from typing import Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from db.models import *
from core.config import get_settings

settings = get_settings()

class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)


app = FastAPI(title=settings.PROJECT_TITLE)

# app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=settings.APP_PORT, workers=settings.APP_WORKERS, reload=True)