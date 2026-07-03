import math
import random
from dataclasses import dataclass, field
from enum import Enum

from app.core.card import Card, Rank, Suit
from app.core.game_state import GameState, PlayerAction
from app.core.hand_evaluator import HandEvaluator


@dataclass(frozen=True)
class ActionCandidate:
    action: PlayerAction
    amount: int | None = None

    def label(self) -> str:
        if self.amount is None:
            return self.action.value

        return f"{self.action.value}_{self.amount}"


@dataclass
class MCTSNode:
    candidate: ActionCandidate | None = None
    parent: "MCTSNode | None" = None
    visits: int = 0
    value: float = 0.0
    children: list["MCTSNode"] = field(default_factory=list)

    def average_value(self) -> float:
        if self.visits == 0:
            return 0.0

        return self.value / self.visits

    def ucb_score(self, exploration: float) -> float:
        if self.visits == 0:
            return float("inf")

        if self.parent is None or self.parent.visits == 0:
            return self.average_value()

        exploration_term = exploration * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )

        return self.average_value() + exploration_term


@dataclass
class MCTSDecision:
    action: PlayerAction
    amount: int | None
    confidence: float
    estimated_value: float
    iterations: int
    reason: str
    tree_summary: list[dict]

    def to_dict(self) -> dict:
        return {
            "strategy": "mcts",
            "action": self.action.value,
            "amount": self.amount,
            "confidence": self.confidence,
            "estimated_value": self.estimated_value,
            "iterations": self.iterations,
            "reason": self.reason,
            "tree_summary": self.tree_summary,
        }


class MCTSPokerBot:
    def __init__(self, iterations: int = 700, exploration: float = 1.414):
        self.iterations = iterations
        self.exploration = exploration

    def decide(self, state: GameState) -> MCTSDecision:
        player_index = state.current_player_index
        candidates = self._candidate_actions(state, player_index)

        if not candidates:
            raise ValueError("AI has no available actions")

        root = MCTSNode()

        for candidate in candidates:
            root.children.append(MCTSNode(candidate=candidate, parent=root))

        for _ in range(self.iterations):
            selected = self._select(root)
            reward = self._simulate_action(state, selected.candidate)
            self._backpropagate(selected, reward)

        best_child = max(
            root.children,
            key=lambda child: (child.average_value(), child.visits),
        )

        if best_child.candidate is None:
            raise ValueError("MCTS failed to select an action")

        confidence = self._confidence(best_child, root)
        tree_summary = self._tree_summary(root)

        return MCTSDecision(
            action=best_child.candidate.action,
            amount=best_child.candidate.amount,
            confidence=confidence,
            estimated_value=round(best_child.average_value(), 4),
            iterations=self.iterations,
            reason=self._reason(best_child, root),
            tree_summary=tree_summary,
        )

    def _candidate_actions(
        self,
        state: GameState,
        player_index: int,
    ) -> list[ActionCandidate]:
        available_actions = state.available_actions(player_index)
        candidates: list[ActionCandidate] = []

        if PlayerAction.FOLD.value in available_actions:
            candidates.append(ActionCandidate(PlayerAction.FOLD))

        if PlayerAction.CHECK.value in available_actions:
            candidates.append(ActionCandidate(PlayerAction.CHECK))

        if PlayerAction.CALL.value in available_actions:
            candidates.append(ActionCandidate(PlayerAction.CALL))

        if PlayerAction.RAISE.value in available_actions:
            candidates.append(
                ActionCandidate(
                    PlayerAction.RAISE,
                    self._raise_to_amount(state, multiplier=3),
                )
            )

        return candidates

    def _select(self, root: MCTSNode) -> MCTSNode:
        if not root.children:
            raise ValueError("Root has no children")

        return max(
            root.children,
            key=lambda child: child.ucb_score(self.exploration),
        )

    def _simulate_action(
        self,
        state: GameState,
        candidate: ActionCandidate | None,
    ) -> float:
        if candidate is None:
            return 0.0

        player_index = state.current_player_index
        to_call = state.call_amount(player_index)
        pot = max(state.pot, 1)

        if candidate.action == PlayerAction.FOLD:
            return -0.65

        outcome = self._random_showdown_outcome(state, player_index)

        if candidate.action == PlayerAction.CHECK:
            reward = outcome

        elif candidate.action == PlayerAction.CALL:
            pot_odds_penalty = min(0.35, to_call / (pot + to_call + 1))
            reward = outcome - pot_odds_penalty

        elif candidate.action == PlayerAction.RAISE:
            player = state.players[player_index]
            additional_risk = max(0, (candidate.amount or 0) - player.current_bet)
            risk_ratio = min(0.5, additional_risk / (pot + additional_risk + 1))

            if outcome > 0:
                reward = outcome + risk_ratio * 0.35
            elif outcome == 0:
                reward = outcome - risk_ratio * 0.15
            else:
                reward = outcome - risk_ratio * 0.35

        else:
            reward = 0.0

        return max(-1.0, min(1.0, reward))

    def _random_showdown_outcome(self, state: GameState, player_index: int) -> float:
        player = state.players[player_index]
        known_cards = player.hole_cards + state.community_cards

        available_cards = self._available_cards(known_cards)
        random.shuffle(available_cards)

        opponent_hole_cards = available_cards[:2]
        cursor = 2

        board_cards_needed = 5 - len(state.community_cards)
        simulated_board = (
            state.community_cards
            + available_cards[cursor : cursor + board_cards_needed]
        )

        player_cards = player.hole_cards + simulated_board
        opponent_cards = opponent_hole_cards + simulated_board

        result = HandEvaluator.compare(player_cards, opponent_cards)

        if result == 1:
            return 1.0

        if result == 0:
            return 0.0

        return -1.0

    def _available_cards(self, known_cards: list[Card]) -> list[Card]:
        known = {(card.rank, card.suit) for card in known_cards}

        return [
            Card(rank, suit)
            for suit in Suit
            for rank in Rank
            if (rank, suit) not in known
        ]

    def _backpropagate(self, node: MCTSNode, reward: float):
        current: MCTSNode | None = node

        while current is not None:
            current.visits += 1
            current.value += reward
            current = current.parent

    def _confidence(self, best_child: MCTSNode, root: MCTSNode) -> float:
        if root.visits == 0:
            return 0.5

        visit_share = best_child.visits / root.visits
        value_strength = abs(best_child.average_value())

        confidence = 0.5 + visit_share * 0.3 + value_strength * 0.2

        return round(max(0.52, min(0.96, confidence)), 2)

    def _tree_summary(self, root: MCTSNode) -> list[dict]:
        summary = []

        for child in sorted(root.children, key=lambda node: node.visits, reverse=True):
            if child.candidate is None:
                continue

            summary.append(
                {
                    "action": child.candidate.action.value,
                    "amount": child.candidate.amount,
                    "visits": child.visits,
                    "average_value": round(child.average_value(), 4),
                }
            )

        return summary

    def _reason(self, best_child: MCTSNode, root: MCTSNode) -> str:
        if best_child.candidate is None:
            return "MCTS could not produce a decision."

        action = best_child.candidate.action.value
        visits = best_child.visits
        average_value = best_child.average_value()

        return (
            f"MCTS selected {action} after {root.visits} rollouts. "
            f"This action received {visits} visits with an average simulated value "
            f"of {average_value:.3f}."
        )

    def _raise_to_amount(self, state: GameState, multiplier: int) -> int:
        minimum_raise_to = state.highest_bet() + state.big_blind
        target_raise_to = state.highest_bet() + state.big_blind * multiplier

        return max(minimum_raise_to, target_raise_to)
