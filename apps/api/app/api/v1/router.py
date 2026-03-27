from fastapi import APIRouter
from app.api.v1.endpoints import diamond
from app.api.v1.endpoints import worker
from app.api.v1.endpoints import assignment
from app.api.v1.endpoints import dashboard
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import location, alert, process





api_router = APIRouter()

api_router.include_router(diamond.router, prefix="/diamond")
api_router.include_router(worker.router, prefix="/worker")
api_router.include_router(assignment.router, prefix="/assignment")

api_router.include_router(dashboard.router, prefix="/dashboard")

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router.include_router(location.router, prefix="/worker", tags=["location"])
api_router.include_router(alert.router, prefix="/dashboard", tags=["alerts"])
api_router.include_router(process.router, prefix="/process", tags=["process"])