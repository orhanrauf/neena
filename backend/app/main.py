from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import SessionLocal

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Custom exception handler for RequestValidationError
@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
# @app.exception_handler(StarletteHTTPException)
async def validation_exception_handler(request, exc):
    error_messages = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_messages.append({field: message})

    return JSONResponse(
        status_code=422,  # HTTP status code for Unprocessable Entity
        content={"errors": error_messages}
    )

# Set all CORS enabled originsf
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    print
    try:
        init_db(db)
    finally:
        db.close()