from app.db.client import db
from datetime import datetime, timezone
from pymongo import DESCENDING


def savePublicMessage(message):
    message["timestamp"] = datetime.now(timezone.utc)
    # Save the message to the database
    try:
        db.public_chat_messages.insert_one(message)
        keep_last_100() # Ensure we only keep the last 100 messages in the public chat
        print(f"Message saved to DB: {message}")
    except Exception as e:
        print(f"Error saving message to DB: {e}")
        raise e
    return {"status": "success", "message": "Message saved successfully"}



def keep_last_100(room: str = "public"):
    # find the 100th newest message
    cursor = db.public_chat_messages.find(
        {"room": room},
        {"_id": 1}
    ).sort("timestamp", DESCENDING).skip(99).limit(1)

    doc = next(cursor, None)
    if not doc:
        return  # less than 100 messages

    cutoff_id = doc["_id"]

    # delete anything older than that
    db.public_chat_messages.delete_many({
        "room": room,
        "_id": {"$lt": cutoff_id}
    })
    

def get_public_messages(limit: int = 100):
    msgs = list(
        db.public_chat_messages
          .find({"room": "public"})
          .sort("timestamp", DESCENDING)
          .limit(limit)
    )

    # make JSON-safe
    for m in msgs:
        m["_id"] = str(m["_id"])
        m["timestamp"] = m["timestamp"].isoformat()

    return list(reversed(msgs))  # oldest -> newest 