import random
from dataclasses import dataclass

from app.core.card import Card, Rank, Suit
from app.core.game_state import GameState, PlayerAction
from app.core.hand_evaluator import HandEvaluator


@dataclass
class MonteCarloDecision:
    action: PlayerAction
    amount: int | None
    confidence: float
    equity: float
    simulations: int
    reason: str

    def to_dict(self) -> dict:
        return {
            "strategy": "monte_carlo",
            "action": self.action.value,
            "amount": self.amount,
            "confidence": self.confidence,
            "equity": self.equity,
            "simulations": self.simulations,
            "reason": self.reason,
        }


class MonteCarloPokerBot:
    def __init__(self, simulations: int = 500):
        self.simulations = simulations

    def decide(self, state: GameState) -> MonteCarloDecision:
        player_index = state.current_player_index
        available_actions = state.available_actions(player_index)

        if not available_actions:
            raise ValueError("AI has no available actions")

        equity = self.estimate_equity(state, player_index, self.simulations)
        to_call = state.call_amount(player_index)

        confidence = self._confidence_from_equity(equity)

        if equity >= 0.72 and PlayerAction.RAISE.value in available_actions:
            raise_to = self._raise_to_amount(state, multiplier=3)
            return MonteCarloDecision(
                action=PlayerAction.RAISE,
                amount=raise_to,
                confidence=confidence,
                equity=equity,
                simulations=self.simulations,
                reason=f"Monte Carlo equity is high at {equity:.1%}. AI raises for value.",
            )

        if equity >= 0.48:
            if to_call > 0 and PlayerAction.CALL.value in available_actions:
                return MonteCarloDecision(
                    action=PlayerAction.CALL,
                    amount=None,
                    confidence=confidence,
                    equity=equity,
                    simulations=self.simulations,
                    reason=f"Monte Carlo equity is playable at {equity:.1%}. AI calls.",
                )

            if PlayerAction.CHECK.value in available_actions:
                return MonteCarloDecision(
                    action=PlayerAction.CHECK,
                    amount=None,
                    confidence=confidence,
                    equity=equity,
                    simulations=self.simulations,
                    reason=f"Monte Carlo equity is stable at {equity:.1%}. AI checks.",
                )

        if equity >= 0.34:
            if PlayerAction.CHECK.value in available_actions:
                return MonteCarloDecision(
                    action=PlayerAction.CHECK,
                    amount=None,
                    confidence=confidence,
                    equity=equity,
                    simulations=self.simulations,
                    reason=f"Monte Carlo equity is marginal at {equity:.1%}. AI checks to control the pot.",
                )

            if to_call <= state.big_blind and PlayerAction.CALL.value in available_actions:
                return MonteCarloDecision(
                    action=PlayerAction.CALL,
                    amount=None,
                    confidence=confidence,
                    equity=equity,
                    simulations=self.simulations,
                    reason=f"Monte Carlo equity is marginal at {equity:.1%}, but the call is cheap.",
                )

        if PlayerAction.CHECK.value in available_actions:
            return MonteCarloDecision(
                action=PlayerAction.CHECK,
                amount=None,
                confidence=confidence,
                equity=equity,
                simulations=self.simulations,
                reason=f"Monte Carlo equity is weak at {equity:.1%}, but checking is free.",
            )

        return MonteCarloDecision(
            action=PlayerAction.FOLD,
            amount=None,
            confidence=confidence,
            equity=equity,
            simulations=self.simulations,
            reason=f"Monte Carlo equity is low at {equity:.1%}. AI folds to pressure.",
        )

    def estimate_equity(
        self,
        state: GameState,
        player_index: int,
        simulations: int | None = None,
    ) -> float:
        total_simulations = simulations or self.simulations

        if total_simulations <= 0:
            raise ValueError("Simulations must be greater than zero")

        player = state.players[player_index]
        known_cards = player.hole_cards + state.community_cards

        wins = 0
        ties = 0

        for _ in range(total_simulations):
            available_cards = self._available_cards(known_cards)
            random.shuffle(available_cards)

            opponent_hole_cards = available_cards[:2]
            cursor = 2

            cards_needed_for_board = 5 - len(state.community_cards)
            simulated_board = (
                state.community_cards
                + available_cards[cursor : cursor + cards_needed_for_board]
            )

            player_cards = player.hole_cards + simulated_board
            opponent_cards = opponent_hole_cards + simulated_board

            result = HandEvaluator.compare(player_cards, opponent_cards)

            if result == 1:
                wins += 1
            elif result == 0:
                ties += 1

        return (wins + ties * 0.5) / total_simulations

    def _available_cards(self, known_cards: list[Card]) -> list[Card]:
        known = {(card.rank, card.suit) for card in known_cards}

        return [
            Card(rank, suit)
            for suit in Suit
            for rank in Rank
            if (rank, suit) not in known
        ]

    def _confidence_from_equity(self, equity: float) -> float:
        distance_from_even = abs(equity - 0.5)
        confidence = 0.55 + distance_from_even

        return round(min(0.95, max(0.52, confidence)), 2)

    def _raise_to_amount(self, state: GameState, multiplier: int) -> int:
        minimum_raise_to = state.highest_bet() + state.big_blind
        target_raise_to = state.highest_bet() + state.big_blind * multiplier

        return max(minimum_raise_to, target_raise_to)
