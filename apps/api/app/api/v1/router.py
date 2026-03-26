from fastapi import APIRouter
from app.api.v1.endpoints import diamond

api_router = APIRouter()

api_router.include_router(diamond.router, prefix="/diamond")