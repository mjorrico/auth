from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["websockets"])


@router.websocket("/ws/echo")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive data from the client
            data = await websocket.receive_text()
            # Send data back
            await websocket.send_text(f"Router received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
