from fastapi import APIRouter

from app.api.api_v1.endpoints import myfinance

api_router = APIRouter()

api_router.include_router(myfinance.router, prefix='/myfinance', tags=['myfinance'])
