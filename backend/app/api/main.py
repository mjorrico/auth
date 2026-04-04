from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import (
    healthcheck,
    websocket,
    auth,
    simple_task_router,
)

app = FastAPI(title="Authy")

app.include_router(healthcheck.router, prefix="/api/v1")
app.include_router(websocket.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(simple_task_router.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Authy is running!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
