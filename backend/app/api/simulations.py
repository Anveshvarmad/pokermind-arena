from fastapi import APIRouter, HTTPException

from app.api.schemas import SimulationRequest
from app.services.simulation_service import simulation_service

router = APIRouter(prefix="/simulations", tags=["Simulations"])


@router.post("/run")
def run_simulation(payload: SimulationRequest):
    try:
        return simulation_service.run_simulation(
            hands=payload.hands,
            player_a_strategy=payload.player_a_strategy,
            player_b_strategy=payload.player_b_strategy,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
