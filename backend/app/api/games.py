from fastapi import APIRouter, HTTPException

from app.api.schemas import CreateGameRequest, PlayerActionRequest
from app.services.game_service import game_service

router = APIRouter(prefix="/games", tags=["Games"])


@router.post("")
def create_game(payload: CreateGameRequest):
    try:
        return game_service.create_game(
            player_names=payload.player_names,
            starting_stack=payload.starting_stack,
            small_blind=payload.small_blind,
            big_blind=payload.big_blind,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/{game_id}")
def get_game(game_id: str):
    game = game_service.get_game(game_id)

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    return game


@router.post("/{game_id}/action")
def apply_action(game_id: str, payload: PlayerActionRequest):
    try:
        game = game_service.apply_action(
            game_id=game_id,
            player_index=payload.player_index,
            action=payload.action,
            amount=payload.amount,
        )

        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")

        return game

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/{game_id}/ai-action")
def apply_ai_action(game_id: str):
    try:
        game = game_service.apply_ai_action(game_id)

        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")

        return game

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/{game_id}/monte-carlo-action")
def apply_monte_carlo_action(game_id: str):
    try:
        game = game_service.apply_monte_carlo_action(game_id)

        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")

        return game

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/{game_id}/mcts-action")
def apply_mcts_action(game_id: str):
    try:
        game = game_service.apply_mcts_action(game_id)

        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")

        return game

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/{game_id}/next-street")
def next_street(game_id: str):
    try:
        game = game_service.next_street(game_id)

        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")

        return game

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/{game_id}/reset")
def reset_game(game_id: str):
    game = game_service.reset_game(game_id)

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    return game
