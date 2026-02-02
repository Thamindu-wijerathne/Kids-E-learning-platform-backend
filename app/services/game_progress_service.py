from app.db.client import db
from datetime import datetime

def update_game_progress(email: str, progress: dict):
    game = progress["game"]

    db.users.update_one(
        {"email": email},
        {
            "$set": {
                f"game_progress.{game}": progress
            }
        },
        upsert=False
    )


def get_game_progress(email: str, game_name: str):
    user = db.users.find_one({"email": email})
    if not user:
        return None
    return user.get("game_progress", {}).get(game_name)
