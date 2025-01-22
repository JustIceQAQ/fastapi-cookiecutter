from fastapi import APIRouter
from configs.settings import get_settings
from .sechemas import GetStatusResponse

status_router = APIRouter(prefix="/status", tags=["Status"])

runtime_settings = get_settings()


@status_router.get("/", response_model=GetStatusResponse)
async def get_status():
    return GetStatusResponse(runserver_datetime=runtime_settings.RUNSERVER_DATETIME)
