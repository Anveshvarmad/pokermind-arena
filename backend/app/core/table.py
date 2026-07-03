from app.core.game_state import GameState
from app.core.player import Player


class PokerTable:
    def __init__(
        self,
        player_names: list[str] | None = None,
        starting_stack: int = 1000,
        small_blind: int = 10,
        big_blind: int = 20,
    ):
        if player_names is None:
            player_names = ["You", "AI Bot"]

        if len(player_names) < 2:
            raise ValueError("Poker table requires at least two players")

        self.players = [
            Player(id=f"player_{index + 1}", name=name, stack=starting_stack)
            for index, name in enumerate(player_names)
        ]

        self.state = GameState(
            players=self.players,
            small_blind=small_blind,
            big_blind=big_blind,
        )

    def start_hand(self) -> GameState:
        self.state.start_new_hand()
        return self.state

    def get_state(self) -> dict:
        return self.state.to_dict()
