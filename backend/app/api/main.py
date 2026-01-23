from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from routers import healthcheck, websocket

app = FastAPI(title="Websocket Test API")

app.include_router(healthcheck.router, prefix="/api/v1")
app.include_router(websocket.router, prefix="/api/v1")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Add websocket to schema
    openapi_schema["paths"]["/api/v1/ws/echo"] = {
        "get": {
            "tags": ["websockets"],
            "summary": "Websocket Echo",
            "description": "Establish a websocket connection for echoing messages.",
            "responses": {"101": {"description": "Switching Protocols"}},
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI app"}
