import logging
import traceback

from time import sleep
from app.modules.celery_app import CeleryApp
from celery.states import SUCCESS, STARTED, PENDING, FAILURE

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)
celery_app = CeleryApp()


@celery_app.task(name="simple.ocr", bind=True)
def simple_ocr_task(self, **params):
    page = -1
    pages = params.get("pages", 0)
    try:
        pages = params.pop("pages")
        difficulty = params.pop("difficulty")
        is_failed = params.pop("is_failed", False)  # simulate failure
        for page in range(pages):
            self.update_state(
                state="PROGRESS",
                meta={
                    "current": page + 1,
                    "total": pages,
                    "percent": round(((page + 1) / pages) * 100) if pages > 0 else 0,
                    "status": f"Processed page {page + 1} of {pages}",
                },
            )
            if is_failed and page == pages // 2:
                raise RuntimeError("Test task failed")
            logger.warning(f"Page {page} out of {pages}")
            sleep(difficulty)
        return {  # this one auto updates state to SUCCESS
            "current": pages if pages > 0 else 0,
            "total": pages if pages > 0 else 0,
            "percent": 100,
            "status": "Test task is completed",
        }
    except Exception as e:
        raise RuntimeError(
            {
                "current": page + 1 if page != -1 else 0,
                "total": pages,
                "percent": round(((page + 1) / pages) * 100) if pages > 0 else 0,
                "status": "Error",
                "message": str(e),
                "traceback": traceback.format_exc(),
            }
        ) from e
