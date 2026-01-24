import os

from fastapi import FastAPI

from app.api.routers import (
    healthcheck,
    websocket,
    auth,
)

app = FastAPI(title="Authy")

app.include_router(healthcheck.router, prefix="/api/v1")
app.include_router(websocket.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Authy is running!"}
