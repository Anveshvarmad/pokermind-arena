from dataclasses import dataclass, field

from app.core.card import Card


@dataclass
class Player:
    id: str
    name: str
    stack: int = 1000
    hole_cards: list[Card] = field(default_factory=list)
    current_bet: int = 0
    total_committed: int = 0
    folded: bool = False
    all_in: bool = False

    def reset_for_new_hand(self):
        self.hole_cards = []
        self.current_bet = 0
        self.total_committed = 0
        self.folded = False
        self.all_in = False

    def reset_for_new_street(self):
        self.current_bet = 0

    def receive_cards(self, cards: list[Card]):
        self.hole_cards.extend(cards)

    def place_bet(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("Bet amount cannot be negative")

        actual_amount = min(amount, self.stack)

        self.stack -= actual_amount
        self.current_bet += actual_amount
        self.total_committed += actual_amount

        if self.stack == 0:
            self.all_in = True

        return actual_amount

    def fold(self):
        self.folded = True

    def to_public_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "stack": self.stack,
            "current_bet": self.current_bet,
            "total_committed": self.total_committed,
            "folded": self.folded,
            "all_in": self.all_in,
            "hole_cards": [card.to_dict() for card in self.hole_cards],
        }
