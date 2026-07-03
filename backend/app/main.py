from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.games import router as games_router
from app.api.health import router as health_router

app = FastAPI(
    title="PokerMind Arena API",
    description="AI-powered Texas Hold'em poker simulator backend.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(games_router, prefix="/api")


@app.get("/")
def root():
    return {
        "name": "PokerMind Arena",
        "status": "running",
        "message": "AI poker simulator backend is live.",
    }
