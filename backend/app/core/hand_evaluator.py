from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
from itertools import combinations

from app.core.card import Card


class HandCategory(IntEnum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9


CATEGORY_LABELS = {
    HandCategory.HIGH_CARD: "High Card",
    HandCategory.PAIR: "Pair",
    HandCategory.TWO_PAIR: "Two Pair",
    HandCategory.THREE_OF_A_KIND: "Three of a Kind",
    HandCategory.STRAIGHT: "Straight",
    HandCategory.FLUSH: "Flush",
    HandCategory.FULL_HOUSE: "Full House",
    HandCategory.FOUR_OF_A_KIND: "Four of a Kind",
    HandCategory.STRAIGHT_FLUSH: "Straight Flush",
}


@dataclass(frozen=True)
class HandEvaluation:
    category: HandCategory
    rank_values: tuple[int, ...]
    cards: tuple[Card, ...]

    def score(self) -> tuple[int, tuple[int, ...]]:
        return int(self.category), self.rank_values

    def label(self) -> str:
        return CATEGORY_LABELS[self.category]

    def to_dict(self) -> dict:
        return {
            "category": self.category.name.lower(),
            "label": self.label(),
            "rank_values": list(self.rank_values),
            "cards": [card.to_dict() for card in self.cards],
            "score": [int(self.category), list(self.rank_values)],
        }


class HandEvaluator:
    @staticmethod
    def evaluate(cards: list[Card]) -> HandEvaluation:
        if len(cards) < 5:
            raise ValueError("At least 5 cards are required to evaluate a hand")

        if len(cards) > 7:
            raise ValueError("At most 7 cards can be evaluated")

        best_hand: HandEvaluation | None = None

        for five_cards in combinations(cards, 5):
            current = HandEvaluator._evaluate_five_cards(tuple(five_cards))

            if best_hand is None or current.score() > best_hand.score():
                best_hand = current

        if best_hand is None:
            raise ValueError("Unable to evaluate hand")

        return best_hand

    @staticmethod
    def compare(first_cards: list[Card], second_cards: list[Card]) -> int:
        first = HandEvaluator.evaluate(first_cards)
        second = HandEvaluator.evaluate(second_cards)

        if first.score() > second.score():
            return 1

        if first.score() < second.score():
            return -1

        return 0

    @staticmethod
    def find_winner(player_hands: dict[str, list[Card]]) -> dict:
        if not player_hands:
            raise ValueError("At least one player hand is required")

        evaluations = {
            player_id: HandEvaluator.evaluate(cards)
            for player_id, cards in player_hands.items()
        }

        best_score = max(evaluation.score() for evaluation in evaluations.values())

        winners = [
            player_id
            for player_id, evaluation in evaluations.items()
            if evaluation.score() == best_score
        ]

        return {
            "winners": winners,
            "evaluations": {
                player_id: evaluation.to_dict()
                for player_id, evaluation in evaluations.items()
            },
        }

    @staticmethod
    def _evaluate_five_cards(cards: tuple[Card, ...]) -> HandEvaluation:
        values = sorted((card.value for card in cards), reverse=True)
        counts = Counter(values)

        groups = sorted(
            counts.items(),
            key=lambda item: (item[1], item[0]),
            reverse=True,
        )

        is_flush = len({card.suit for card in cards}) == 1
        straight_high = HandEvaluator._straight_high(values)
        is_straight = straight_high is not None

        if is_straight and is_flush:
            return HandEvaluation(
                HandCategory.STRAIGHT_FLUSH,
                (straight_high,),
                cards,
            )

        if groups[0][1] == 4:
            four_rank = groups[0][0]
            kicker = max(value for value in values if value != four_rank)
            return HandEvaluation(
                HandCategory.FOUR_OF_A_KIND,
                (four_rank, kicker),
                cards,
            )

        if groups[0][1] == 3 and groups[1][1] == 2:
            return HandEvaluation(
                HandCategory.FULL_HOUSE,
                (groups[0][0], groups[1][0]),
                cards,
            )

        if is_flush:
            return HandEvaluation(
                HandCategory.FLUSH,
                tuple(values),
                cards,
            )

        if is_straight:
            return HandEvaluation(
                HandCategory.STRAIGHT,
                (straight_high,),
                cards,
            )

        if groups[0][1] == 3:
            three_rank = groups[0][0]
            kickers = sorted(
                [value for value in values if value != three_rank],
                reverse=True,
            )

            return HandEvaluation(
                HandCategory.THREE_OF_A_KIND,
                (three_rank, *kickers),
                cards,
            )

        pair_ranks = sorted(
            [rank for rank, count in counts.items() if count == 2],
            reverse=True,
        )

        if len(pair_ranks) == 2:
            kicker = max(value for value in values if value not in pair_ranks)
            return HandEvaluation(
                HandCategory.TWO_PAIR,
                (pair_ranks[0], pair_ranks[1], kicker),
                cards,
            )

        if len(pair_ranks) == 1:
            pair_rank = pair_ranks[0]
            kickers = sorted(
                [value for value in values if value != pair_rank],
                reverse=True,
            )

            return HandEvaluation(
                HandCategory.PAIR,
                (pair_rank, *kickers),
                cards,
            )

        return HandEvaluation(
            HandCategory.HIGH_CARD,
            tuple(values),
            cards,
        )

    @staticmethod
    def _straight_high(values: list[int]) -> int | None:
        unique_values = sorted(set(values), reverse=True)

        if len(unique_values) != 5:
            return None

        if unique_values == [14, 5, 4, 3, 2]:
            return 5

        if unique_values[0] - unique_values[-1] == 4:
            return unique_values[0]

        return None
