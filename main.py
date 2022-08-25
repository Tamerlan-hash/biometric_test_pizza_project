from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from settings.database import async_engine
from settings.database.connection import Base

from app.views import pizza_router, restaurant_router

openapi_json_url = "/openapi.json"
title = "Pizza API"

app = FastAPI(
    title=title, redoc_url=None, docs_url=None, openapi_url=openapi_json_url
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(pizza_router)
app.include_router(restaurant_router)
add_pagination(app)


@app.get("/redoc", include_in_schema=False)
async def overridden_redoc():
    return get_redoc_html(
        openapi_url=openapi_json_url,
        title=title,
    )


@app.get("/docs", include_in_schema=False)
async def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url=openapi_json_url,
        title=title,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors_dict = {"detail": []}
    for error in exc.errors():
        err = {error["loc"][1]: error["msg"]}
        errors_dict["detail"].append(err)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=errors_dict,
    )


@app.on_event("startup")
async def startup():
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    pass
