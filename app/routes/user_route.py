from fastapi import APIRouter, Depends
from app.utils.jwt import get_current_user
from app.db.client import db

router = APIRouter()

@router.get("/profile")
async def get_profile(user=Depends(get_current_user)):
    user = user["email"]
    db.users.aggregate([
        {
            "$match": {"email": user}
        },
        {
            "$project": {"email": 1, "name": 1, "role": 1}
        },
        {
            "$project": {
                "email": 1,
                "name": 1,
                "totalScore": {"$sum": "$gamesArray.v.scoreDelta"},
                "gameCount": {"$size": "$gamesArray"}
            }
        }
    ])
    return user
