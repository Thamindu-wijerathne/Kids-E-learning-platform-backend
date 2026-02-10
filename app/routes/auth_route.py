from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
from app.services.auth_service import authenticate_user, create_user
from app.utils.jwt import create_access_token
from app.schemas.auth_schema import LoginRequest, LoginResponse, LoginResponse, SignupResponse, SignupRequest

router = APIRouter()


@router.post("/signup", response_model=SignupResponse)
def signup(data: SignupRequest):
    print("Signup data received:", data)
    try:
        user = create_user(data.name, data.email, data.password, data.age_group)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    token = create_access_token({"email": user["email"]})
    return {"user": user, "access_token": token}

@router.post("/login", response_model=SignupResponse)
def login(data: LoginRequest):
    user = authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"email": user["email"]})
    return {"user": user, "access_token": token}