import json
from typing import Dict, Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import end_edit, get_active_editors, start_edit
from database import get_db, async_session

router = APIRouter()

# Connected clients: {websocket: username}
clients: Dict[WebSocket, str] = {}


async def broadcast(message: dict, exclude: WebSocket | None = None):
    payload = json.dumps(message, ensure_ascii=False)
    for ws in list(clients):
        if ws is exclude:
            continue
        try:
            await ws.send_text(payload)
        except Exception:
            clients.pop(ws, None)


async def send_active_editors():
    async with async_session() as db:
        editors = await get_active_editors(db)
    await broadcast({"type": "ACTIVE_EDITORS", "editors": editors})


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, username: str = "anonymous"):
    await websocket.accept()
    clients[websocket] = username

    # Send current editors on connect
    await send_active_editors()

    try:
        while True:
            text = await websocket.receive_text()
            data = json.loads(text)
            msg_type = data.get("type")
            req_id = data.get("req_id")

            if msg_type == "EDITING_START" and req_id:
                async with async_session() as db:
                    ok = await start_edit(db, req_id, username)
                if ok:
                    await send_active_editors()
                else:
                    await websocket.send_text(json.dumps({
                        "type": "EDIT_DENIED",
                        "req_id": req_id,
                        "message": "Someone else is editing this requirement",
                    }))

            elif msg_type == "EDITING_END" and req_id:
                async with async_session() as db:
                    await end_edit(db, req_id, username)
                await send_active_editors()

            elif msg_type == "REQ_UPDATED" and req_id:
                await broadcast(
                    {"type": "REQ_UPDATED", "req_id": req_id, "updated_by": username},
                    exclude=websocket,
                )

    except WebSocketDisconnect:
        clients.pop(websocket, None)
        # Clean up any edit sessions for this user
        async with async_session() as db:
            editors = await get_active_editors(db)
            for rid, uname in editors.items():
                if uname == username:
                    await end_edit(db, rid, username)
        await send_active_editors()
