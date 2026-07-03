import random

from app.core.card import Card, Rank, Suit


class Deck:
    def __init__(self):
        self.cards: list[Card] = []
        self.reset()

    def reset(self):
        self.cards = [Card(rank, suit) for suit in Suit for rank in Rank]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, count: int = 1) -> list[Card]:
        if count <= 0:
            raise ValueError("Count must be greater than zero")

        if count > len(self.cards):
            raise ValueError("Not enough cards left in deck")

        drawn_cards = self.cards[:count]
        self.cards = self.cards[count:]
        return drawn_cards

    def remaining(self) -> int:
        return len(self.cards)
