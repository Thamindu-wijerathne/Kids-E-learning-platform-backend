from fastapi import APIRouter, Depends
from app.utils.jwt import get_current_user
from app.db.client import db

router = APIRouter()

@router.get("/profile")
async def get_profile(current_user=Depends(get_current_user)):
    email = current_user["email"]

    pipeline = [
        {"$match": {"email": email}},
        {
            "$project": {
                "_id": 0,
                "email": 1,
                "name": 1,
                "role": 1,
                "gamesArray": {
                    "$ifNull": [
                        {"$objectToArray": "$game_progress"},
                        []
                    ]
                }
            }
        },
        {
            "$project": {
                "email": 1,
                "name": 1,
                "role": 1,
                "totalScore": {"$sum": "$gamesArray.v.scoreDelta"},
                "totalTimeSpent": {"$sum": "$gamesArray.v.timeSpent"},
                "gameCount": {"$size": "$gamesArray"},
                "games": {"$ifNull": ["$game_progress", {}]}
            }
        }
    ]

    result = list(db.users.aggregate(pipeline))

    return result[0] if result else {}
