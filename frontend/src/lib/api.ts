import type { GameState, PlayerActionPayload } from "../types/game";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

async function handleResponse(response: Response): Promise<GameState> {
  const data = await response.json();

  if (!response.ok) {
    const message = data?.detail ?? "Something went wrong";
    throw new Error(message);
  }

  return data;
}

export async function createGame(): Promise<GameState> {
  const response = await fetch(`${API_BASE_URL}/api/games`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      player_names: ["You", "AI Bot"],
      starting_stack: 1000,
      small_blind: 10,
      big_blind: 20,
    }),
  });

  return handleResponse(response);
}

export async function getGame(gameId: string): Promise<GameState> {
  const response = await fetch(`${API_BASE_URL}/api/games/${gameId}`);

  return handleResponse(response);
}

export async function applyPlayerAction(
  gameId: string,
  payload: PlayerActionPayload,
): Promise<GameState> {
  const response = await fetch(`${API_BASE_URL}/api/games/${gameId}/action`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  return handleResponse(response);
}

export async function applyAiAction(gameId: string): Promise<GameState> {
  const response = await fetch(`${API_BASE_URL}/api/games/${gameId}/ai-action`, {
    method: "POST",
  });

  return handleResponse(response);
}

export async function nextStreet(gameId: string): Promise<GameState> {
  const response = await fetch(`${API_BASE_URL}/api/games/${gameId}/next-street`, {
    method: "POST",
  });

  return handleResponse(response);
}

export async function resetGame(gameId: string): Promise<GameState> {
  const response = await fetch(`${API_BASE_URL}/api/games/${gameId}/reset`, {
    method: "POST",
  });

  return handleResponse(response);
}
