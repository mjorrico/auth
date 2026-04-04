from celery import Celery

import os

CELERY_BROKER_ADDRESS = str(os.environ["CELERY_BROKER_ADDRESS"])
CELERY_BACKEND_ADDRESS = str(os.environ["CELERY_BACKEND_ADDRESS"])


class CeleryApp(Celery):
    def __init__(self):
        self.app_name = "celery-app"
        super().__init__(
            self.app_name,
            broker=CELERY_BROKER_ADDRESS,
            backend=CELERY_BACKEND_ADDRESS,
        )
        self.conf.update(
            task_track_started=True,  # Enables the STARTED state
            task_acks_late=True,  # Task only acknowledged after completion (safer)
            task_reject_on_worker_lost=True,  # Re-queues task if worker dies mid-execution
        )
