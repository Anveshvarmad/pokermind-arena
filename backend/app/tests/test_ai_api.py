from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ai_action_after_player_call():
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
    assert player_response.json()["current_player_name"] == "AI Bot"

    ai_response = client.post(f"/api/games/{game_id}/ai-action")

    assert ai_response.status_code == 200

    data = ai_response.json()

    assert "ai_decision" in data
    assert data["ai_decision"]["action"] in ["fold", "check", "call", "raise"]
    assert "reason" in data["ai_decision"]


def test_ai_action_rejects_when_not_ai_turn():
    create_response = client.post("/api/games", json={})
    game_id = create_response.json()["game_id"]

    response = client.post(f"/api/games/{game_id}/ai-action")

    assert response.status_code == 400
    assert response.json()["detail"] == "It is not the AI bot's turn"
