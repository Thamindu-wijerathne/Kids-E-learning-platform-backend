from fastapi import APIRouter, Depends
from app.utils.jwt import get_current_user
from app.db.client import db
from app.schemas.user_schema import CustomizationRequest

router = APIRouter()

@router.put("/customizations")
async def update_customizations(data: CustomizationRequest, current_user=Depends(get_current_user)):
    email = current_user["email"]
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    
    if update_data:
        set_fields = {f"customizations.{k}": v for k, v in update_data.items()}
        db.users.update_one(
            {"email": email},
            {"$set": set_fields}
        )
    
    return {"status": "success", "message": "Customizations updated"}

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
                "customizations": {"$ifNull": ["$customizations", {}]},
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
                "customizations": 1,
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
