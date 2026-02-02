from fastapi import APIRouter, HTTPException, Depends
from app.utils.jwt import get_current_user
from app.services.game_progress_service import update_game_progress

router = APIRouter()

@router.post("/save-progress")
def save_progress(progress: dict, user=Depends(get_current_user)):
    email = user["email"]
    update_game_progress(email, progress)
    # print("email : ", email)
    # print("progress : ", progress)

    return {"message": "Progress saved successfully"}
