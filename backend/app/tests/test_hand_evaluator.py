from app.core.card import Card, Rank, Suit
from app.core.hand_evaluator import HandCategory, HandEvaluator


def c(rank: Rank, suit: Suit) -> Card:
    return Card(rank, suit)


def test_high_card():
    cards = [
        c(Rank.ACE, Suit.SPADES),
        c(Rank.KING, Suit.HEARTS),
        c(Rank.NINE, Suit.CLUBS),
        c(Rank.SEVEN, Suit.DIAMONDS),
        c(Rank.THREE, Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.category == HandCategory.HIGH_CARD
    assert result.rank_values == (14, 13, 9, 7, 3)


def test_pair():
    cards = [
        c(Rank.ACE, Suit.SPADES),
        c(Rank.ACE, Suit.HEARTS),
        c(Rank.NINE, Suit.CLUBS),
        c(Rank.SEVEN, Suit.DIAMONDS),
        c(Rank.THREE, Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.category == HandCategory.PAIR
    assert result.rank_values == (14, 9, 7, 3)


def test_two_pair():
    cards = [
        c(Rank.ACE, Suit.SPADES),
        c(Rank.ACE, Suit.HEARTS),
        c(Rank.NINE, Suit.CLUBS),
        c(Rank.NINE, Suit.DIAMONDS),
        c(Rank.THREE, Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.category == HandCategory.TWO_PAIR
    assert result.rank_values == (14, 9, 3)


def test_three_of_a_kind():
    cards = [
        c(Rank.QUEEN, Suit.SPADES),
        c(Rank.QUEEN, Suit.HEARTS),
        c(Rank.QUEEN, Suit.CLUBS),
        c(Rank.NINE, Suit.DIAMONDS),
        c(Rank.THREE, Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.category == HandCategory.THREE_OF_A_KIND
    assert result.rank_values == (12, 9, 3)


def test_straight():
    cards = [
        c(Rank.NINE, Suit.SPADES),
        c(Rank.EIGHT, Suit.HEARTS),
        c(Rank.SEVEN, Suit.CLUBS),
        c(Rank.SIX, Suit.DIAMONDS),
        c(Rank.FIVE, Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.category == HandCategory.STRAIGHT
    assert result.rank_values == (9,)


def test_wheel_straight():
    cards = [
        c(Rank.ACE, Suit.SPADES),
        c(Rank.FIVE, Suit.HEARTS),
        c(Rank.FOUR, Suit.CLUBS),
        c(Rank.THREE, Suit.DIAMONDS),
        c(Rank.TWO, Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.category == HandCategory.STRAIGHT
    assert result.rank_values == (5,)


def test_flush():
    cards = [
        c(Rank.ACE, Suit.HEARTS),
        c(Rank.QUEEN, Suit.HEARTS),
        c(Rank.NINE, Suit.HEARTS),
        c(Rank.SEVEN, Suit.HEARTS),
        c(Rank.THREE, Suit.HEARTS),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.category == HandCategory.FLUSH
    assert result.rank_values == (14, 12, 9, 7, 3)


def test_full_house():
    cards = [
        c(Rank.KING, Suit.SPADES),
        c(Rank.KING, Suit.HEARTS),
        c(Rank.KING, Suit.CLUBS),
        c(Rank.THREE, Suit.DIAMONDS),
        c(Rank.THREE, Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.category == HandCategory.FULL_HOUSE
    assert result.rank_values == (13, 3)


def test_four_of_a_kind():
    cards = [
        c(Rank.TEN, Suit.SPADES),
        c(Rank.TEN, Suit.HEARTS),
        c(Rank.TEN, Suit.CLUBS),
        c(Rank.TEN, Suit.DIAMONDS),
        c(Rank.THREE, Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.category == HandCategory.FOUR_OF_A_KIND
    assert result.rank_values == (10, 3)


def test_straight_flush():
    cards = [
        c(Rank.NINE, Suit.SPADES),
        c(Rank.EIGHT, Suit.SPADES),
        c(Rank.SEVEN, Suit.SPADES),
        c(Rank.SIX, Suit.SPADES),
        c(Rank.FIVE, Suit.SPADES),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.category == HandCategory.STRAIGHT_FLUSH
    assert result.rank_values == (9,)


def test_best_hand_from_seven_cards():
    cards = [
        c(Rank.ACE, Suit.SPADES),
        c(Rank.ACE, Suit.HEARTS),
        c(Rank.ACE, Suit.CLUBS),
        c(Rank.KING, Suit.SPADES),
        c(Rank.KING, Suit.HEARTS),
        c(Rank.TWO, Suit.CLUBS),
        c(Rank.THREE, Suit.DIAMONDS),
    ]

    result = HandEvaluator.evaluate(cards)

    assert result.category == HandCategory.FULL_HOUSE
    assert result.rank_values == (14, 13)


def test_compare_hands():
    first = [
        c(Rank.ACE, Suit.SPADES),
        c(Rank.ACE, Suit.HEARTS),
        c(Rank.NINE, Suit.CLUBS),
        c(Rank.SEVEN, Suit.DIAMONDS),
        c(Rank.THREE, Suit.SPADES),
    ]

    second = [
        c(Rank.KING, Suit.SPADES),
        c(Rank.KING, Suit.HEARTS),
        c(Rank.NINE, Suit.CLUBS),
        c(Rank.SEVEN, Suit.DIAMONDS),
        c(Rank.THREE, Suit.SPADES),
    ]

    assert HandEvaluator.compare(first, second) == 1


def test_find_winner():
    player_hands = {
        "player_1": [
            c(Rank.ACE, Suit.SPADES),
            c(Rank.ACE, Suit.HEARTS),
            c(Rank.NINE, Suit.CLUBS),
            c(Rank.SEVEN, Suit.DIAMONDS),
            c(Rank.THREE, Suit.SPADES),
        ],
        "player_2": [
            c(Rank.KING, Suit.SPADES),
            c(Rank.KING, Suit.HEARTS),
            c(Rank.NINE, Suit.CLUBS),
            c(Rank.SEVEN, Suit.DIAMONDS),
            c(Rank.THREE, Suit.SPADES),
        ],
    }

    result = HandEvaluator.find_winner(player_hands)

    assert result["winners"] == ["player_1"]
    assert result["evaluations"]["player_1"]["label"] == "Pair"
