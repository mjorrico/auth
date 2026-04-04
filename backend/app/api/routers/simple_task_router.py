from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from celery.result import AsyncResult

from app.workers.simple import simple_ocr_task
from app.modules.celery_app import CeleryApp

router = APIRouter(tags=["simple_task"])
celery_app = CeleryApp()


class TestTaskRequest(BaseModel):
    pages: int = 10
    difficulty: int = 3
    is_failed: bool = False


@router.post("/test-task")
async def trigger_test_task(request: TestTaskRequest):
    task = simple_ocr_task.apply_async(
        kwargs={
            "pages": request.pages,
            "difficulty": request.difficulty,
            "is_failed": request.is_failed,
        },
        queue="simple",
    )
    return {
        "status": "success",
        "message": "Test task dispatched",
        "task_id": str(task.id),
    }


from celery.result import AsyncResult


@router.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    if result.state == "PENDING":
        return {
            "state": "PENDING",
            "percent": 0,
            "status": "Waiting in queue...",
        }

    elif result.state == "STARTED":
        return {
            "state": "STARTED",
            "percent": 0,
            "status": "Worker has picked up the task...",
        }

    elif result.state == "PROGRESS":
        info = result.info if isinstance(result.info, dict) else {}
        return {
            "state": "PROGRESS",
            "percent": info.get("percent"),
            "current": info.get("current"),
            "total": info.get("total"),
            "status": info.get("status"),
        }

    elif result.state == "SUCCESS":
        info = result.info if isinstance(result.info, dict) else {}
        return {
            "state": "SUCCESS",
            "percent": 100,
            "current": info.get("current"),
            "total": info.get("total"),
            "status": info.get("status"),
        }

    elif result.state == "FAILURE":
        info = result.info
        # Celery stores the exception in result.info on FAILURE
        if isinstance(info, Exception):
            # If the exception was raised with a dictionary as its first argument
            if hasattr(info, "args") and info.args and isinstance(info.args[0], dict):
                info = info.args[0]
            else:
                info = {
                    "status": "Error",
                    "message": str(info),
                }

        # Ensure info is a dict for .get()
        if not isinstance(info, dict):
            info = {}

        return {
            "state": "FAILURE",
            "percent": -1,
            "current": info.get("current"),
            "total": info.get("total"),
            "status": info.get("status"),
        }

    # Catch-all for REVOKED or any unexpected state
    return {
        "state": result.state,
        "status": "Unknown state.",
    }
