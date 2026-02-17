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
                "gamesArray": {
                    "$ifNull": [
                        {"$objectToArray": "$games"},
                        []
                    ]
                }
            }
        },
        {
            "$project": {
                "email": 1,
                "name": 1,
                "gameCount": {"$size": "$gamesArray"},
                "games": {"$ifNull": ["$games", {}]},
                "totalScore": {
                    "$sum": {
                        "$map": {
                        "input": "$gamesArray",
                        "as": "g",
                        "in": {
                            "$ifNull": [
                            "$$g.v.scores.totalScore",
                            { "$ifNull": [
                                "$$g.v.scores.highScore",
                                { "$ifNull": ["$$g.v.scores.lastScore", 0] }
                            ]}
                            ]
                        }
                        }
                    }
                },
                "totalTimeSpent": {
                    "$sum": {
                        "$map": {
                            "input": "$gamesArray",
                            "as": "g",
                            "in": { "$ifNull": ["$$g.v.timeSpent", 0] }
                        }
                    }
                }
            }
        }
    ]

    result = list(db.users.aggregate(pipeline))

    return result[0] if result else {}
