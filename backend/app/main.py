from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.games import router as games_router
from app.api.health import router as health_router
from app.api.history import router as history_router
from app.api.simulations import router as simulations_router
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="PokerMind Arena API",
    description="AI-powered Texas Hold'em poker simulator backend.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(games_router, prefix="/api")
app.include_router(simulations_router, prefix="/api")
app.include_router(history_router, prefix="/api")


@app.get("/")
def root():
    return {
        "name": "PokerMind Arena",
        "status": "running",
        "message": "AI poker simulator backend is live.",
    }
