from fastapi import APIRouter, HTTPException, Depends
from app.utils.jwt import get_current_user
from app.services.game_progress_service import (
    update_game_progress, 
    get_game_progress,
    update_word_builder_progress,
    get_level,
    get_score,
    save_level,
    save_score,
    get_all_game_progress
)

router = APIRouter()

@router.get("/get-progress/all")
def get_all_progress(user=Depends(get_current_user)):
    email = user["email"]
    progress = get_all_game_progress(email)
    return progress

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

@router.post("/scores/{game_id}")
def save_game_score(game_id: str, data: dict, user=Depends(get_current_user)):
    # Save score for a game
    email = user["email"]
    score = data.get("score", 0)
    scoring_type = data.get("type", "session")
    
    result = save_score(email, game_id, score, scoring_type)
    return result

@router.get("/scores/{game_id}")
def get_game_score(game_id: str, user=Depends(get_current_user)):
    # Get score data for a game
    email = user["email"]
    return get_score(email, game_id)



@router.post("/levels/{game_id}")
def save_game_level(game_id: str, data: dict, user=Depends(get_current_user)):
    # Save level for a game
    email = user["email"]
    level = data.get("level", 1)
    
    result = save_level(email, game_id, level)
    return result

@router.get("/levels/{game_id}")
def get_game_level(game_id: str, user=Depends(get_current_user)):
    # Get level for a game
    email = user["email"]
    return get_level(email, game_id)




