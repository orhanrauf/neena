from app.core.logging import logger
import time
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from opencensus.ext.azure.log_exporter import AzureLogHandler
import traceback
import os

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
#TODO Set this to the actual origin of the fronetend from GitHub Actions
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://neenacoredevwebst.z6.web.core.windows.net",  # Production origin
        "http://localhost:5173",  # Development origin
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

if settings.LOG_APPINSIGHTS:        
    ai_handler = AzureLogHandler(connection_string=settings.APPLICATIONINSIGHTS_CONNECTION_STRING)
    logger.addHandler(ai_handler)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Handled request {request.method} {request.url} in {duration:.2f} seconds. Response code: {response.status_code}")

    return response
    
# Add exception handling to also log it
@app.middleware("http")
async def exception_logging_middleware(request: Request, call_next):
    try:
        # Try processing the request
        response = await call_next(request)
        return response
    except Exception as exc:
        # Log the exception with traceback
        logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")

        # Return a generic error response
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"}
        )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
        
