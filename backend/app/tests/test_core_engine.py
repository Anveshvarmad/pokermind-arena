from app.core.card import Card, Rank, Suit
from app.core.deck import Deck
from app.core.player import Player
from app.core.table import PokerTable


def test_card_display_and_value():
    card = Card(Rank.ACE, Suit.SPADES)

    assert card.value == 14
    assert card.display() == "A♠"


def test_deck_has_52_unique_cards():
    deck = Deck()

    cards = deck.draw(52)
    unique_cards = {(card.rank, card.suit) for card in cards}

    assert len(cards) == 52
    assert len(unique_cards) == 52
    assert deck.remaining() == 0


def test_player_can_receive_cards_and_bet():
    player = Player(id="player_1", name="You", stack=1000)
    cards = [
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.KING, Suit.HEARTS),
    ]

    player.receive_cards(cards)
    amount = player.place_bet(100)

    assert amount == 100
    assert player.stack == 900
    assert player.current_bet == 100
    assert player.total_committed == 100
    assert len(player.hole_cards) == 2


def test_table_starts_hand_with_blinds_and_hole_cards():
    table = PokerTable()
    state = table.start_hand()

    assert state.street.value == "preflop"
    assert state.pot == 30
    assert len(state.players) == 2
    assert len(state.players[0].hole_cards) == 2
    assert len(state.players[1].hole_cards) == 2
    assert state.deck.remaining() == 48
    assert state.players[0].stack == 990
    assert state.players[1].stack == 980


def test_deal_flop_turn_and_river():
    table = PokerTable()
    state = table.start_hand()

    state.deal_flop()
    assert state.street.value == "flop"
    assert len(state.community_cards) == 3
    assert state.deck.remaining() == 45

    state.deal_turn()
    assert state.street.value == "turn"
    assert len(state.community_cards) == 4
    assert state.deck.remaining() == 44

    state.deal_river()
    assert state.street.value == "river"
    assert len(state.community_cards) == 5
    assert state.deck.remaining() == 43
