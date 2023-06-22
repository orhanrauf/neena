from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# # Custom exception handler for RequestValidationError
# @app.exception_handler(RequestValidationError)
# @app.exception_handler(ValidationError)
# # @app.exception_handler(StarletteHTTPException)
# async def validation_exception_handler(request, exc):
#     error_messages = []
#     for error in exc.errors():
#         field = ".".join(str(loc) for loc in error["loc"])
#         message = error["msg"]
#         error_messages.append({field: message})

#     return JSONResponse(
#         status_code=422,  # HTTP status code for Unprocessable Entity
#         content={"errors": error_messages}
#     )

# Set all CORS enabled originsf
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
