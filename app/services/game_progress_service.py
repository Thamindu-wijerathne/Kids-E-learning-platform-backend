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

def update_word_builder_progress(email: str, progress: dict):
    game = "Word Builder"
    db.users.update_one(
        {"email": email},
        {
            "$set": {
                f"game_progress.{game}.game": game,
                f"game_progress.{game}.level": progress["level"],
                f"game_progress.{game}.difficulty": progress["difficulty"],
                f"game_progress.{game}.scoreDelta": progress["scoreDelta"],
                f"game_progress.{game}.word": progress.get("word"),
                f"game_progress.{game}.isCorrect": progress.get("isCorrect"),
                f"game_progress.{game}.lastPlayed": datetime.now(),
            },
            "$inc": {
                f"game_progress.{game}.timeSpent": progress.get("timeSpent", 0)
            }
        }
    )
    
def update_speech_explorer_progress(email: str, progress: dict):
    game = "Speech Explorer"
    db.users.update_one(
        {"email": email},
        {
            "$set": {
                f"game_progress.{game}.game": game,
                f"game_progress.{game}.level": progress["level"],
                f"game_progress.{game}.score": progress["score"],
                f"game_progress.{game}.targetWord": progress.get("targetWord"),
                f"game_progress.{game}.recognizedText": progress.get("recognizedText"),
                f"game_progress.{game}.index": progress.get("index"),
                f"game_progress.{game}.lastPlayed": datetime.now(),
            },
            # "$inc": {
            #     f"game_progress.{game}.timeSpent": progress.get("timeSpent", 0)
            # }
        }
    )

def get_game_progress(email: str, game_name: str):
    user = db.users.find_one({"email": email})
    if not user:
        return None
    return user.get("game_progress", {}).get(game_name)



def save_score(email: str, game_id: str, score: int, scoring_type: str):
    user = db.users.find_one({"email": email}) or {}
    score_data = user.get("games", {}).get(game_id, {}).get("scores", {})

    if scoring_type == "highest":
        current_high = score_data.get("highScore", 0)
        new_high = max(current_high, score)

        db.users.update_one(
            {"email": email},
            {"$set": {
                f"games.{game_id}.scores.highScore": new_high,
                f"games.{game_id}.scores.lastScore": score,
                f"games.{game_id}.lastPlayed": datetime.now()
            }}
        )
        return {"highScore": new_high, "lastScore": score}

    elif scoring_type == "persistent":
        current_total = score_data.get("totalScore", 0)
        new_total = current_total + score

        db.users.update_one(
            {"email": email},
            {"$set": {
                f"games.{game_id}.scores.totalScore": new_total,
                f"games.{game_id}.lastPlayed": datetime.now()
            }}
        )
        return {"totalScore": new_total}

    else:
        db.users.update_one(
            {"email": email},
            {"$set": {
                f"games.{game_id}.scores.lastScore": score,
                f"games.{game_id}.lastPlayed": datetime.now()
            }}
        )
        return {"lastScore": score}


def get_score(email: str, game_id: str):
    user = db.users.find_one({"email": email}) or {}
    score_data = user.get("games", {}).get(game_id, {}).get("scores", {})
    return {
        "totalScore": score_data.get("totalScore", 0),
        "highScore": score_data.get("highScore", 0),
        "lastScore": score_data.get("lastScore", 0),
    }

def save_level(email: str, game_id: str, level: int):
    db.users.update_one(
        {"email": email},
        {"$set": {
            f"games.{game_id}.level": level,
            f"games.{game_id}.lastPlayed": datetime.now()
        }}
    )
    return {"level": level}


def get_level(email: str, game_id: str):
    user = db.users.find_one({"email": email}) or {}
    return {"level": user.get("games", {}).get(game_id, {}).get("level", 1)}
    

