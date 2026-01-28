from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_route

app = FastAPI(title="E-Learning Platform API")

# Enable CORS for frontend
origins = [
    "http://localhost:3000",  # Next.js dev server
    "http://127.0.0.1:3000",
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

@app.get("/")
def root():
    return {"message": "FastAPI running"}
