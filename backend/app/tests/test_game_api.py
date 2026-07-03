from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_game():
    response = client.post("/api/games", json={})

    assert response.status_code == 200

    data = response.json()

    assert data["street"] == "preflop"
    assert data["pot"] == 30
    assert len(data["players"]) == 2
    assert len(data["players"][0]["hole_cards"]) == 2
    assert len(data["players"][1]["hole_cards"]) == 2
    assert data["deck_remaining"] == 48


def test_get_game():
    create_response = client.post("/api/games", json={})
    game_id = create_response.json()["game_id"]

    get_response = client.get(f"/api/games/{game_id}")

    assert get_response.status_code == 200
    assert get_response.json()["game_id"] == game_id


def test_player_call_action():
    create_response = client.post("/api/games", json={})
    game = create_response.json()
    game_id = game["game_id"]

    response = client.post(
        f"/api/games/{game_id}/action",
        json={
            "player_index": 0,
            "action": "call",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["pot"] == 40
    assert data["players"][0]["current_bet"] == 20
    assert data["players"][0]["stack"] == 980


def test_player_raise_action():
    create_response = client.post("/api/games", json={})
    game = create_response.json()
    game_id = game["game_id"]

    response = client.post(
        f"/api/games/{game_id}/action",
        json={
            "player_index": 0,
            "action": "raise",
            "amount": 60,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["pot"] == 80
    assert data["players"][0]["current_bet"] == 60
    assert data["players"][0]["stack"] == 940


def test_next_street():
    create_response = client.post("/api/games", json={})
    game_id = create_response.json()["game_id"]

    flop_response = client.post(f"/api/games/{game_id}/next-street")

    assert flop_response.status_code == 200
    assert flop_response.json()["street"] == "flop"
    assert len(flop_response.json()["community_cards"]) == 3

    turn_response = client.post(f"/api/games/{game_id}/next-street")

    assert turn_response.status_code == 200
    assert turn_response.json()["street"] == "turn"
    assert len(turn_response.json()["community_cards"]) == 4

    river_response = client.post(f"/api/games/{game_id}/next-street")

    assert river_response.status_code == 200
    assert river_response.json()["street"] == "river"
    assert len(river_response.json()["community_cards"]) == 5


def test_invalid_game_returns_404():
    response = client.get("/api/games/not-real")

    assert response.status_code == 404
