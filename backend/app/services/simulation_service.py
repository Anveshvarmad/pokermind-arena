import random
from collections import Counter

from app.core.card import Card, Rank, Suit
from app.core.deck import Deck
from app.core.hand_evaluator import HandCategory, HandEvaluator


class SimulationService:
    def run_simulation(
        self,
        hands: int,
        player_a_strategy: str,
        player_b_strategy: str,
    ) -> dict:
        bankroll_a = 1000
        bankroll_b = 1000

        wins = Counter()
        action_distribution = {
            "player_a": Counter(),
            "player_b": Counter(),
        }

        bankroll_history = []
        hand_results = []

        for hand_number in range(1, hands + 1):
            deck = Deck()

            player_a_hole = deck.draw(2)
            player_b_hole = deck.draw(2)

            board = deck.draw(5)

            winner = None
            street_actions = []

            streets = [
                ("preflop", []),
                ("flop", board[:3]),
                ("turn", board[:4]),
                ("river", board[:5]),
            ]

            for street, community_cards in streets:
                action_a = self._choose_action(
                    strategy=player_a_strategy,
                    hole_cards=player_a_hole,
                    community_cards=community_cards,
                    street=street,
                )

                action_distribution["player_a"][action_a] += 1
                street_actions.append(
                    {
                        "street": street,
                        "player": "player_a",
                        "strategy": player_a_strategy,
                        "action": action_a,
                    }
                )

                if action_a == "fold":
                    winner = "player_b"
                    break

                action_b = self._choose_action(
                    strategy=player_b_strategy,
                    hole_cards=player_b_hole,
                    community_cards=community_cards,
                    street=street,
                )

                action_distribution["player_b"][action_b] += 1
                street_actions.append(
                    {
                        "street": street,
                        "player": "player_b",
                        "strategy": player_b_strategy,
                        "action": action_b,
                    }
                )

                if action_b == "fold":
                    winner = "player_a"
                    break

            player_a_eval = HandEvaluator.evaluate(player_a_hole + board)
            player_b_eval = HandEvaluator.evaluate(player_b_hole + board)

            if winner is None:
                result = HandEvaluator.compare(player_a_hole + board, player_b_hole + board)

                if result == 1:
                    winner = "player_a"
                elif result == -1:
                    winner = "player_b"
                else:
                    winner = "tie"

            if winner == "player_a":
                bankroll_a += 20
                bankroll_b -= 20
                wins["player_a"] += 1
            elif winner == "player_b":
                bankroll_a -= 20
                bankroll_b += 20
                wins["player_b"] += 1
            else:
                wins["tie"] += 1

            bankroll_history.append(
                {
                    "hand": hand_number,
                    "player_a": bankroll_a,
                    "player_b": bankroll_b,
                }
            )

            hand_results.append(
                {
                    "hand": hand_number,
                    "winner": winner,
                    "player_a_cards": [card.to_dict() for card in player_a_hole],
                    "player_b_cards": [card.to_dict() for card in player_b_hole],
                    "community_cards": [card.to_dict() for card in board],
                    "player_a_best_hand": player_a_eval.to_dict(),
                    "player_b_best_hand": player_b_eval.to_dict(),
                    "actions": street_actions,
                    "bankroll_after": {
                        "player_a": bankroll_a,
                        "player_b": bankroll_b,
                    },
                }
            )

        return {
            "hands": hands,
            "player_a_strategy": player_a_strategy,
            "player_b_strategy": player_b_strategy,
            "wins": {
                "player_a": wins["player_a"],
                "player_b": wins["player_b"],
                "tie": wins["tie"],
            },
            "win_rates": {
                "player_a": round(wins["player_a"] / hands, 4),
                "player_b": round(wins["player_b"] / hands, 4),
                "tie": round(wins["tie"] / hands, 4),
            },
            "final_bankroll": {
                "player_a": bankroll_a,
                "player_b": bankroll_b,
            },
            "bankroll_history": bankroll_history,
            "action_distribution": {
                "player_a": dict(action_distribution["player_a"]),
                "player_b": dict(action_distribution["player_b"]),
            },
            "recent_hands": hand_results[-10:],
        }

    def _choose_action(
        self,
        strategy: str,
        hole_cards: list[Card],
        community_cards: list[Card],
        street: str,
    ) -> str:
        if strategy == "rule_based":
            return self._rule_based_action(hole_cards, community_cards, street)

        if strategy == "monte_carlo":
            return self._monte_carlo_action(hole_cards, community_cards, street)

        if strategy == "mcts":
            return self._mcts_style_action(hole_cards, community_cards, street)

        raise ValueError("Unsupported simulation strategy")

    def _rule_based_action(
        self,
        hole_cards: list[Card],
        community_cards: list[Card],
        street: str,
    ) -> str:
        if street == "preflop":
            score = self._preflop_score(hole_cards)

            if score >= 72:
                return "raise"

            if score >= 42:
                return "call"

            return "fold"

        strength = self._made_hand_strength(hole_cards, community_cards)

        if strength >= HandCategory.TWO_PAIR:
            return "raise"

        if strength >= HandCategory.PAIR:
            return "call"

        return "check"

    def _monte_carlo_action(
        self,
        hole_cards: list[Card],
        community_cards: list[Card],
        street: str,
    ) -> str:
        equity = self._estimate_equity(hole_cards, community_cards, simulations=90)

        if equity >= 0.68:
            return "raise"

        if equity >= 0.43:
            return "call" if street == "preflop" else "check"

        if street == "preflop":
            return "fold"

        return "check"

    def _mcts_style_action(
        self,
        hole_cards: list[Card],
        community_cards: list[Card],
        street: str,
    ) -> str:
        candidates = ["fold", "call", "raise"] if street == "preflop" else ["check", "call", "raise"]
        scores = {}

        for candidate in candidates:
            total = 0.0

            for _ in range(80):
                equity = self._estimate_equity(hole_cards, community_cards, simulations=1)

                if candidate == "fold":
                    reward = -0.55
                elif candidate == "check":
                    reward = equity - 0.45
                elif candidate == "call":
                    reward = equity - 0.5
                else:
                    reward = equity - 0.52
                    if equity > 0.6:
                        reward += 0.18

                total += reward

            scores[candidate] = total / 80

        return max(scores, key=scores.get)

    def _preflop_score(self, cards: list[Card]) -> int:
        first, second = sorted(cards, key=lambda card: card.value, reverse=True)

        high = first.value
        low = second.value
        is_pair = first.value == second.value
        is_suited = first.suit == second.suit
        gap = high - low

        if is_pair:
            return min(100, 42 + high * 4)

        score = high * 3 + low * 2

        if is_suited:
            score += 8

        if gap == 1:
            score += 7
        elif gap == 2:
            score += 4
        elif gap >= 5:
            score -= 8

        if high == 14:
            score += 8

        if high >= 13 and low >= 10:
            score += 10

        return max(0, min(100, score))

    def _made_hand_strength(
        self,
        hole_cards: list[Card],
        community_cards: list[Card],
    ) -> HandCategory:
        cards = hole_cards + community_cards

        if len(cards) < 5:
            score = self._preflop_score(hole_cards)

            if score >= 72:
                return HandCategory.PAIR

            return HandCategory.HIGH_CARD

        return HandEvaluator.evaluate(cards).category

    def _estimate_equity(
        self,
        hole_cards: list[Card],
        community_cards: list[Card],
        simulations: int,
    ) -> float:
        known_cards = hole_cards + community_cards
        wins = 0
        ties = 0

        for _ in range(simulations):
            available_cards = self._available_cards(known_cards)
            random.shuffle(available_cards)

            opponent_hole = available_cards[:2]
            cursor = 2

            cards_needed = 5 - len(community_cards)
            board = community_cards + available_cards[cursor : cursor + cards_needed]

            result = HandEvaluator.compare(hole_cards + board, opponent_hole + board)

            if result == 1:
                wins += 1
            elif result == 0:
                ties += 1

        return (wins + ties * 0.5) / simulations

    def _available_cards(self, known_cards: list[Card]) -> list[Card]:
        known = {(card.rank, card.suit) for card in known_cards}

        return [
            Card(rank, suit)
            for suit in Suit
            for rank in Rank
            if (rank, suit) not in known
        ]


simulation_service = SimulationService()
