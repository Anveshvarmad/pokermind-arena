from app.ai.mcts_bot import MCTSPokerBot
from app.ai.monte_carlo_bot import MonteCarloPokerBot
from app.ai.rule_based_bot import RuleBasedPokerBot
from app.core.game_state import PlayerAction, Street
from app.core.table import PokerTable
from app.services.history_service import history_service


class GameService:
    def __init__(self):
        self.games: dict[str, PokerTable] = {}
        self.rule_bot = RuleBasedPokerBot()
        self.monte_carlo_bot = MonteCarloPokerBot(simulations=500)
        self.mcts_bot = MCTSPokerBot(iterations=700)

    def create_game(
        self,
        player_names: list[str],
        starting_stack: int,
        small_blind: int,
        big_blind: int,
    ) -> dict:
        table = PokerTable(
            player_names=player_names,
            starting_stack=starting_stack,
            small_blind=small_blind,
            big_blind=big_blind,
        )

        state = table.start_hand()
        self.games[state.game_id] = table

        response = state.to_dict()
        history_service.save_game_state(response)

        return response

    def get_game(self, game_id: str) -> dict | None:
        table = self.games.get(game_id)

        if table is None:
            return None

        return table.get_state()

    def apply_action(
        self,
        game_id: str,
        player_index: int,
        action: str,
        amount: int | None = None,
    ) -> dict | None:
        table = self.games.get(game_id)

        if table is None:
            return None

        table.state.apply_action(
            player_index=player_index,
            action=PlayerAction(action),
            amount=amount,
        )

        response = table.get_state()
        history_service.save_game_state(response)

        return response

    def apply_ai_action(self, game_id: str) -> dict | None:
        table = self.games.get(game_id)

        if table is None:
            return None

        state = table.state
        self._validate_ai_turn(state)

        decision = self.rule_bot.decide(state)

        state.apply_action(
            player_index=state.current_player_index,
            action=decision.action,
            amount=decision.amount,
        )

        response = table.get_state()
        ai_decision = decision.to_dict()
        ai_decision["strategy"] = "rule_based"
        response["ai_decision"] = ai_decision

        history_service.save_game_state(response)
        history_service.save_ai_decision(game_id, ai_decision)

        return response

    def apply_monte_carlo_action(self, game_id: str) -> dict | None:
        table = self.games.get(game_id)

        if table is None:
            return None

        state = table.state
        self._validate_ai_turn(state)

        decision = self.monte_carlo_bot.decide(state)

        state.apply_action(
            player_index=state.current_player_index,
            action=decision.action,
            amount=decision.amount,
        )

        response = table.get_state()
        response["ai_decision"] = decision.to_dict()

        history_service.save_game_state(response)
        history_service.save_ai_decision(game_id, response["ai_decision"])

        return response

    def apply_mcts_action(self, game_id: str) -> dict | None:
        table = self.games.get(game_id)

        if table is None:
            return None

        state = table.state
        self._validate_ai_turn(state)

        decision = self.mcts_bot.decide(state)

        state.apply_action(
            player_index=state.current_player_index,
            action=decision.action,
            amount=decision.amount,
        )

        response = table.get_state()
        response["ai_decision"] = decision.to_dict()

        history_service.save_game_state(response)
        history_service.save_ai_decision(game_id, response["ai_decision"])

        return response

    def next_street(self, game_id: str) -> dict | None:
        table = self.games.get(game_id)

        if table is None:
            return None

        state = table.state

        if state.street == Street.PREFLOP:
            state.deal_flop()
        elif state.street == Street.FLOP:
            state.deal_turn()
        elif state.street == Street.TURN:
            state.deal_river()
        elif state.street == Street.RIVER:
            state.move_to_showdown()
        else:
            raise ValueError("Cannot move to next street from current state")

        response = table.get_state()
        history_service.save_game_state(response)

        return response

    def reset_game(self, game_id: str) -> dict | None:
        table = self.games.get(game_id)

        if table is None:
            return None

        state = table.start_hand()
        response = state.to_dict()
        history_service.save_game_state(response)

        return response

    def _validate_ai_turn(self, state):
        current_player = state.players[state.current_player_index]

        if "ai" not in current_player.name.lower() and "bot" not in current_player.name.lower():
            raise ValueError("It is not the AI bot's turn")


game_service = GameService()
