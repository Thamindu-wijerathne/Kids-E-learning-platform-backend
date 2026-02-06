from fastapi import APIRouter, HTTPException, Depends
from app.utils.jwt import get_current_user
from app.services.game_progress_service import (
    update_game_progress, 
    get_game_progress,
    update_word_builder_progress,
    update_speech_explorer_progress
)

router = APIRouter()

@router.post("/save-progress")
def save_progress(progress: dict, user=Depends(get_current_user)):
    email = user["email"]
    update_game_progress(email, progress)
    return {"message": "Progress saved successfully"}

@router.post("/save-progress/word-builder")
def save_word_builder_progress(progress: dict, user=Depends(get_current_user)):
    email = user["email"]
    update_word_builder_progress(email, progress)
    return {"message": "Word Builder progress saved successfully"}

@router.post("/save-progress/speech-explorer")
def save_speech_explorer_progress(progress: dict, user=Depends(get_current_user)):
    email = user["email"]
    update_speech_explorer_progress(email, progress)
    return {"message": "Speech Explorer progress saved successfully"}

@router.get("/get-progress/{game_name}")
def get_progress(game_name: str, user=Depends(get_current_user)):
    email = user["email"]
    progress = get_game_progress(email, game_name)
    print("progress : ", progress)
    return progress
