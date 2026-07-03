from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_history_summary_after_game_creation():
    create_response = client.post("/api/games", json={})

    assert create_response.status_code == 200

    history_response = client.get("/api/history/summary")

    assert history_response.status_code == 200

    data = history_response.json()

    assert "games" in data
    assert "ai_decisions" in data
    assert "simulations" in data
    assert len(data["games"]) >= 1


def test_history_saves_ai_decision():
    create_response = client.post("/api/games", json={})
    game = create_response.json()
    game_id = game["game_id"]

    player_response = client.post(
        f"/api/games/{game_id}/action",
        json={
            "player_index": 0,
            "action": "call",
        },
    )

    assert player_response.status_code == 200

    ai_response = client.post(f"/api/games/{game_id}/ai-action")

    assert ai_response.status_code == 200

    decisions_response = client.get("/api/history/ai-decisions")

    assert decisions_response.status_code == 200

    data = decisions_response.json()

    assert len(data["items"]) >= 1
    assert data["items"][0]["strategy"] in ["rule_based", "monte_carlo", "mcts"]


def test_history_saves_simulation_result():
    simulation_response = client.post(
        "/api/simulations/run",
        json={
            "hands": 5,
            "player_a_strategy": "rule_based",
            "player_b_strategy": "monte_carlo",
        },
    )

    assert simulation_response.status_code == 200

    history_response = client.get("/api/history/simulations")

    assert history_response.status_code == 200

    data = history_response.json()

    assert len(data["items"]) >= 1
    assert data["items"][0]["hands"] >= 5
