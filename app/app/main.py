from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

import time

app = FastAPI(
    title=settings.PROJECT_NAME,
    # comment out for local testing - sets doc path behind proxy
    # root_path=f'{settings.API_V1_STR}/companies'
)

if settings.DEBUG:
    app.debug = True

@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response



# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=['X-Process-Time'],
    )


app.include_router(api_router)