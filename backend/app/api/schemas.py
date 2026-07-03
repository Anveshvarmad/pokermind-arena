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
