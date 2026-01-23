from fastapi import APIRouter

from fastapi import APIRouter

# Define the tag here once
router = APIRouter(tags=["healthcheck"])


@router.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


@router.get("/status")
async def get_status():
    return {"details": "All systems operational"}
