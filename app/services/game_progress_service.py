from app.db.client import db
from datetime import datetime

def update_game_progress(email: str, progress: dict):
    game = progress["game"]

    db.users.update_one(
        {"email": email},
        {
            "$set": {
                f"game_progress.{game}.game": progress["game"],
                f"game_progress.{game}.level": progress["level"],
                f"game_progress.{game}.difficulty": progress["difficulty"],
                f"game_progress.{game}.scoreDelta": progress["scoreDelta"],
            },
            "$inc": {
                f"game_progress.{game}.timeSpent": progress.get("timeSpent", 0)
            }
        }
    )


def get_game_progress(email: str, game_name: str):
    user = db.users.find_one({"email": email})
    if not user:
        return None
    return user.get("game_progress", {}).get(game_name)
