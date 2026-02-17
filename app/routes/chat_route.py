from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from app.utils.jwt import get_current_user
from pydantic import BaseModel
from app.services.chat_service import get_public_messages, get_public_messages, savePublicMessage
from datetime import datetime, timezone
from bson import ObjectId

class PublicChatReq(BaseModel):
    message: str

router = APIRouter()

clients = set()

@router.websocket("/ws/public")
async def public_chat_ws(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            data = await ws.receive_json()
            print(f"Received message: {data}")

            doc = {
                "message": data.get("message", ""),
                "senderName": data.get("user", "Unknown"),
                "avatar": data.get("avatar", "🙂"),
                "room": "public",
            }

            # Save (this mutates doc by adding datetime timestamp)
            savePublicMessage(doc)

            # Make a JSON-safe payload for websocket
            payload = {
                **doc,
                "timestamp": doc["timestamp"].isoformat(),
                "_id": str(doc["_id"]) if "_id" in doc else None,
            }

            # broadcast to everyone
            for c in list(clients):
                await c.send_json(payload)

    except WebSocketDisconnect:
        clients.remove(ws)
        
@router.post("/public")
async def sendMessageToPublicChat(body: PublicChatReq, current_user=Depends(get_current_user)):
    email = current_user["email"]
    message = body.message

    savePublicMessage(message={"message": message, "sender": email, "avatar": current_user.get("avatar", "🙂")})
    print(f"Received message from {email}: {message}")

    
    return {"message": "Message sent successfully"}

@router.get("/public/history")
def public_chat_history(limit: int = 100):
    public_chat_history = get_public_messages(limit)
    return public_chat_history

