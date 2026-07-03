from app.ai.monte_carlo_bot import MonteCarloPokerBot
from app.core.card import Card, Rank, Suit
from app.core.table import PokerTable


def test_monte_carlo_equity_returns_valid_probability():
    table = PokerTable()
    state = table.start_hand()

    bot = MonteCarloPokerBot(simulations=50)
    equity = bot.estimate_equity(state, player_index=0, simulations=50)

    assert 0 <= equity <= 1


def test_monte_carlo_bot_returns_decision():
    table = PokerTable()
    state = table.start_hand()

    state.apply_action(player_index=0, action="call")

    bot = MonteCarloPokerBot(simulations=50)
    decision = bot.decide(state)

    assert decision.action.value in ["fold", "check", "call", "raise"]
    assert 0 <= decision.equity <= 1
    assert decision.simulations == 50
    assert decision.reason


def test_monte_carlo_strong_hand_has_high_equity():
    table = PokerTable()
    state = table.start_hand()

    ai_player = state.players[1]
    ai_player.hole_cards = [
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.ACE, Suit.HEARTS),
    ]

    state.community_cards = [
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.SEVEN, Suit.DIAMONDS),
    ]

    bot = MonteCarloPokerBot(simulations=100)
    equity = bot.estimate_equity(state, player_index=1, simulations=100)

    assert equity > 0.65
