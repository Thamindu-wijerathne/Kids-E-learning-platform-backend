from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_route
from app.routes import testing_route
from app.routes import ocr_route
from app.routes import game_progress_route
from app.routes import user_route
from app.routes import speech_recognize_route
from app.routes import speech_recognize_route

app = FastAPI(title="E-Learning Platform API")

# Enable CORS for frontend
origins = [
    "http://localhost:3000",  # Next.js dev server
    "http://127.0.0.1:3000",
    "http://34.47.219.216:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Allow these URLs
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, etc.
    allow_headers=["*"],         # Allow headers like Content-Type
)

# Include routes
app.include_router(auth_route.router, prefix="/auth", tags=["auth"])
app.include_router(testing_route.router, prefix="/testing", tags=["testing"])
app.include_router(ocr_route.router, prefix="/ocr", tags=["ocr"])
app.include_router(game_progress_route.router, prefix="/game-progress", tags=["game-progress"])
app.include_router(user_route.router, prefix="/user", tags=["user"])
app.include_router(speech_recognize_route.router, prefix="/speech-recognize", tags=["speech-recognize"])

@app.get("/")
def root():
    return {"message": "FastAPI running"}

