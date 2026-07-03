from dataclasses import dataclass

from app.core.game_state import GameState, PlayerAction, Street
from app.core.hand_evaluator import HandCategory, HandEvaluator
from app.core.player import Player


@dataclass
class BotDecision:
    action: PlayerAction
    amount: int | None
    confidence: float
    reason: str

    def to_dict(self) -> dict:
        return {
            "action": self.action.value,
            "amount": self.amount,
            "confidence": self.confidence,
            "reason": self.reason,
        }


class RuleBasedPokerBot:
    def decide(self, state: GameState) -> BotDecision:
        player_index = state.current_player_index
        player = state.players[player_index]
        available_actions = state.available_actions(player_index)

        if not available_actions:
            raise ValueError("AI has no available actions")

        if state.street == Street.PREFLOP:
            return self._decide_preflop(state, player, available_actions)

        return self._decide_postflop(state, player, available_actions)

    def _decide_preflop(
        self,
        state: GameState,
        player: Player,
        available_actions: list[str],
    ) -> BotDecision:
        score = self._preflop_score(player)
        to_call = state.call_amount(state.current_player_index)

        if score >= 70 and PlayerAction.RAISE.value in available_actions:
            raise_to = self._raise_to_amount(state, multiplier=3)
            return BotDecision(
                action=PlayerAction.RAISE,
                amount=raise_to,
                confidence=0.88,
                reason="Premium preflop hand. AI applies pressure with a raise.",
            )

        if score >= 48:
            if to_call > 0 and PlayerAction.CALL.value in available_actions:
                return BotDecision(
                    action=PlayerAction.CALL,
                    amount=None,
                    confidence=0.72,
                    reason="Playable preflop hand with enough strength to call.",
                )

            if PlayerAction.CHECK.value in available_actions:
                return BotDecision(
                    action=PlayerAction.CHECK,
                    amount=None,
                    confidence=0.7,
                    reason="Playable hand and no bet to call, so AI checks.",
                )

        if score >= 35:
            if PlayerAction.CHECK.value in available_actions:
                return BotDecision(
                    action=PlayerAction.CHECK,
                    amount=None,
                    confidence=0.62,
                    reason="Medium-strength preflop hand. AI checks and keeps pot controlled.",
                )

            if to_call <= state.big_blind and PlayerAction.CALL.value in available_actions:
                return BotDecision(
                    action=PlayerAction.CALL,
                    amount=None,
                    confidence=0.58,
                    reason="Marginal hand, but call amount is small.",
                )

        if PlayerAction.CHECK.value in available_actions:
            return BotDecision(
                action=PlayerAction.CHECK,
                amount=None,
                confidence=0.55,
                reason="Weak hand, but checking is free.",
            )

        return BotDecision(
            action=PlayerAction.FOLD,
            amount=None,
            confidence=0.76,
            reason="Weak preflop hand facing a bet. AI folds.",
        )

    def _decide_postflop(
        self,
        state: GameState,
        player: Player,
        available_actions: list[str],
    ) -> BotDecision:
        cards = player.hole_cards + state.community_cards
        evaluation = HandEvaluator.evaluate(cards)
        category = evaluation.category
        to_call = state.call_amount(state.current_player_index)

        if category >= HandCategory.TWO_PAIR and PlayerAction.RAISE.value in available_actions:
            raise_to = self._raise_to_amount(state, multiplier=3)
            return BotDecision(
                action=PlayerAction.RAISE,
                amount=raise_to,
                confidence=0.86,
                reason=f"Strong made hand: {evaluation.label()}. AI raises for value.",
            )

        if category >= HandCategory.PAIR:
            if to_call > 0 and PlayerAction.CALL.value in available_actions:
                return BotDecision(
                    action=PlayerAction.CALL,
                    amount=None,
                    confidence=0.71,
                    reason=f"Made hand: {evaluation.label()}. AI calls.",
                )

            if PlayerAction.CHECK.value in available_actions:
                return BotDecision(
                    action=PlayerAction.CHECK,
                    amount=None,
                    confidence=0.68,
                    reason=f"Made hand: {evaluation.label()}. AI checks to control the pot.",
                )

        if PlayerAction.CHECK.value in available_actions:
            return BotDecision(
                action=PlayerAction.CHECK,
                amount=None,
                confidence=0.6,
                reason=f"No strong made hand yet: {evaluation.label()}. AI checks.",
            )

        if to_call <= state.big_blind and PlayerAction.CALL.value in available_actions:
            return BotDecision(
                action=PlayerAction.CALL,
                amount=None,
                confidence=0.52,
                reason="Weak hand, but call amount is small.",
            )

        return BotDecision(
            action=PlayerAction.FOLD,
            amount=None,
            confidence=0.74,
            reason=f"Weak postflop hand: {evaluation.label()}. AI folds to pressure.",
        )

    def _preflop_score(self, player: Player) -> int:
        first, second = sorted(player.hole_cards, key=lambda card: card.value, reverse=True)

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

    def _raise_to_amount(self, state: GameState, multiplier: int) -> int:
        minimum_raise_to = state.highest_bet() + state.big_blind
        target_raise_to = state.highest_bet() + state.big_blind * multiplier

        return max(minimum_raise_to, target_raise_to)
