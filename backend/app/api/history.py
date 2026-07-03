from fastapi import APIRouter

from app.services.history_service import history_service

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/summary")
def history_summary():
    return history_service.summary()


@router.get("/games")
def latest_games(limit: int = 10):
    return {
        "items": history_service.latest_games(limit=limit),
    }


@router.get("/ai-decisions")
def latest_ai_decisions(limit: int = 10):
    return {
        "items": history_service.latest_ai_decisions(limit=limit),
    }


@router.get("/simulations")
def latest_simulations(limit: int = 10):
    return {
        "items": history_service.latest_simulations(limit=limit),
    }
