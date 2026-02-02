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
