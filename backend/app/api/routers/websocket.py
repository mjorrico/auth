import asyncio
import random
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/monitor", tags=["System"])


@router.websocket("/health")
async def system_health_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Simulate fetching system data (CPU/RAM)
            cpu_usage = random.randint(20, 80)
            memory_usage = random.randint(40, 90)

            # Create a data payload
            data = {
                "cpu": f"{cpu_usage}%",
                "memory": f"{memory_usage}%",
                "status": "Online",
            }

            # PUSH data to the client
            await websocket.send_json(data)

            # Wait 1 second before the next update
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client stopped monitoring.")
