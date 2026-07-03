from app.ai.mcts_bot import MCTSPokerBot
from app.core.game_state import PlayerAction
from app.core.table import PokerTable


def test_mcts_bot_returns_valid_decision():
    table = PokerTable()
    state = table.start_hand()

    state.apply_action(player_index=0, action=PlayerAction.CALL)

    bot = MCTSPokerBot(iterations=80)
    decision = bot.decide(state)

    assert decision.action.value in ["fold", "check", "call", "raise"]
    assert decision.iterations == 80
    assert 0 <= decision.confidence <= 1
    assert len(decision.tree_summary) > 0
    assert decision.reason


def test_mcts_tree_summary_contains_visits_and_values():
    table = PokerTable()
    state = table.start_hand()

    state.apply_action(player_index=0, action=PlayerAction.CALL)

    bot = MCTSPokerBot(iterations=80)
    decision = bot.decide(state)

    first_item = decision.tree_summary[0]

    assert "action" in first_item
    assert "visits" in first_item
    assert "average_value" in first_item
    assert first_item["visits"] > 0


def test_mcts_candidate_actions_do_not_mutate_game_state():
    table = PokerTable()
    state = table.start_hand()

    original_pot = state.pot
    original_street = state.street
    original_current_player = state.current_player_index

    state.apply_action(player_index=0, action=PlayerAction.CALL)

    pot_after_call = state.pot

    bot = MCTSPokerBot(iterations=80)
    bot.decide(state)

    assert state.pot == pot_after_call
    assert state.street == original_street
    assert state.current_player_index != original_current_player
