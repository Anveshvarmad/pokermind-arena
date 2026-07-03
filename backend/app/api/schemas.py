from typing import Literal

from pydantic import BaseModel, Field


class CreateGameRequest(BaseModel):
    player_names: list[str] = Field(default_factory=lambda: ["You", "AI Bot"])
    starting_stack: int = 1000
    small_blind: int = 10
    big_blind: int = 20


class PlayerActionRequest(BaseModel):
    player_index: int
    action: Literal["fold", "check", "call", "raise"]
    amount: int | None = None


class SimulationRequest(BaseModel):
    hands: int = Field(default=100, ge=1, le=1000)
    player_a_strategy: Literal["rule_based", "monte_carlo", "mcts"] = "rule_based"
    player_b_strategy: Literal["rule_based", "monte_carlo", "mcts"] = "monte_carlo"
