from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

from app.core.card import Card
from app.core.deck import Deck
from app.core.player import Player


class Street(str, Enum):
    WAITING = "waiting"
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    SHOWDOWN = "showdown"


class PlayerAction(str, Enum):
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    RAISE = "raise"


@dataclass
class GameState:
    players: list[Player]
    small_blind: int = 10
    big_blind: int = 20
    game_id: str = field(default_factory=lambda: str(uuid4()))
    dealer_index: int = 0
    current_player_index: int = 0
    pot: int = 0
    community_cards: list[Card] = field(default_factory=list)
    street: Street = Street.WAITING
    deck: Deck = field(default_factory=Deck)
    hand_number: int = 0

    def start_new_hand(self):
        self.hand_number += 1
        self.pot = 0
        self.community_cards = []
        self.street = Street.PREFLOP
        self.deck = Deck()

        for player in self.players:
            player.reset_for_new_hand()

        self._deal_hole_cards()
        self._post_blinds()

        if len(self.players) == 2:
            self.current_player_index = self.dealer_index
        else:
            self.current_player_index = self._next_active_player_index(
                (self.dealer_index + 1) % len(self.players)
            )

    def _deal_hole_cards(self):
        for _ in range(2):
            for player in self.players:
                player.receive_cards(self.deck.draw(1))

    def _post_blinds(self):
        if len(self.players) < 2:
            raise ValueError("At least two players are required")

        small_blind_index = self.dealer_index
        big_blind_index = (self.dealer_index + 1) % len(self.players)

        small_blind_amount = self.players[small_blind_index].place_bet(self.small_blind)
        big_blind_amount = self.players[big_blind_index].place_bet(self.big_blind)

        self.pot += small_blind_amount + big_blind_amount

    def highest_bet(self) -> int:
        return max(player.current_bet for player in self.players)

    def call_amount(self, player_index: int) -> int:
        player = self.players[player_index]
        return max(0, self.highest_bet() - player.current_bet)

    def available_actions(self, player_index: int) -> list[str]:
        if self.street in {Street.WAITING, Street.SHOWDOWN}:
            return []

        player = self.players[player_index]

        if player.folded or player.all_in:
            return []

        to_call = self.call_amount(player_index)

        if to_call == 0:
            return [PlayerAction.CHECK.value, PlayerAction.RAISE.value, PlayerAction.FOLD.value]

        return [PlayerAction.FOLD.value, PlayerAction.CALL.value, PlayerAction.RAISE.value]

    def apply_action(
        self,
        player_index: int,
        action: PlayerAction,
        amount: int | None = None,
    ):
        if self.street in {Street.WAITING, Street.SHOWDOWN}:
            raise ValueError("No player action is allowed at this stage")

        if player_index < 0 or player_index >= len(self.players):
            raise ValueError("Invalid player index")

        if player_index != self.current_player_index:
            raise ValueError("It is not this player's turn")

        player = self.players[player_index]

        if player.folded:
            raise ValueError("Folded player cannot act")

        if player.all_in:
            raise ValueError("All-in player cannot act")

        to_call = self.call_amount(player_index)

        if action == PlayerAction.FOLD:
            player.fold()

        elif action == PlayerAction.CHECK:
            if to_call > 0:
                raise ValueError("Player cannot check while facing a bet")

        elif action == PlayerAction.CALL:
            if to_call == 0:
                raise ValueError("Nothing to call")

            committed = player.place_bet(to_call)
            self.pot += committed

        elif action == PlayerAction.RAISE:
            if amount is None:
                raise ValueError("Raise amount is required")

            if amount <= self.highest_bet():
                raise ValueError("Raise amount must be greater than current highest bet")

            additional_amount = amount - player.current_bet

            if additional_amount <= 0:
                raise ValueError("Raise amount must increase player's current bet")

            committed = player.place_bet(additional_amount)
            self.pot += committed

        else:
            raise ValueError("Unsupported action")

        if len(self.active_players()) == 1:
            self.street = Street.SHOWDOWN
            return

        self.current_player_index = self._next_active_player_index(self.current_player_index)

    def deal_flop(self):
        self._move_to_next_street(Street.FLOP, 3)

    def deal_turn(self):
        self._move_to_next_street(Street.TURN, 1)

    def deal_river(self):
        self._move_to_next_street(Street.RIVER, 1)

    def move_to_showdown(self):
        self.street = Street.SHOWDOWN

    def _move_to_next_street(self, street: Street, cards_to_deal: int):
        if self.street == Street.SHOWDOWN:
            raise ValueError("Hand is already complete")

        self.street = street

        for player in self.players:
            player.reset_for_new_street()

        self.community_cards.extend(self.deck.draw(cards_to_deal))
        self.current_player_index = self._next_active_player_index(self.dealer_index)

    def _next_active_player_index(self, start_index: int) -> int:
        total_players = len(self.players)

        for offset in range(1, total_players + 1):
            index = (start_index + offset) % total_players
            player = self.players[index]

            if not player.folded and not player.all_in:
                return index

        return start_index

    def active_players(self) -> list[Player]:
        return [player for player in self.players if not player.folded]

    def to_dict(self) -> dict:
        current_player = self.players[self.current_player_index]

        return {
            "game_id": self.game_id,
            "hand_number": self.hand_number,
            "street": self.street.value,
            "dealer_index": self.dealer_index,
            "current_player_index": self.current_player_index,
            "current_player_id": current_player.id,
            "current_player_name": current_player.name,
            "pot": self.pot,
            "small_blind": self.small_blind,
            "big_blind": self.big_blind,
            "highest_bet": self.highest_bet(),
            "call_amount": self.call_amount(self.current_player_index),
            "available_actions": self.available_actions(self.current_player_index),
            "hand_complete": self.street == Street.SHOWDOWN or len(self.active_players()) == 1,
            "deck_remaining": self.deck.remaining(),
            "community_cards": [card.to_dict() for card in self.community_cards],
            "players": [player.to_public_dict() for player in self.players],
        }
