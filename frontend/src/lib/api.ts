import type { GameState, PlayerActionPayload } from "../types/game";
import type { HistorySummary } from "../types/history";
import type { SimulationResult, StrategyName } from "../types/simulation";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

async function parseResponse<T>(response: Response): Promise<T> {
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

  return parseResponse<GameState>(response);
}

export async function getGame(gameId: string): Promise<GameState> {
  const response = await fetch(`${API_BASE_URL}/api/games/${gameId}`);

  return parseResponse<GameState>(response);
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

  return parseResponse<GameState>(response);
}

export async function applyAiAction(gameId: string): Promise<GameState> {
  const response = await fetch(`${API_BASE_URL}/api/games/${gameId}/ai-action`, {
    method: "POST",
  });

  return parseResponse<GameState>(response);
}

export async function applyMonteCarloAction(gameId: string): Promise<GameState> {
  const response = await fetch(`${API_BASE_URL}/api/games/${gameId}/monte-carlo-action`, {
    method: "POST",
  });

  return parseResponse<GameState>(response);
}

export async function applyMctsAction(gameId: string): Promise<GameState> {
  const response = await fetch(`${API_BASE_URL}/api/games/${gameId}/mcts-action`, {
    method: "POST",
  });

  return parseResponse<GameState>(response);
}

export async function nextStreet(gameId: string): Promise<GameState> {
  const response = await fetch(`${API_BASE_URL}/api/games/${gameId}/next-street`, {
    method: "POST",
  });

  return parseResponse<GameState>(response);
}

export async function resetGame(gameId: string): Promise<GameState> {
  const response = await fetch(`${API_BASE_URL}/api/games/${gameId}/reset`, {
    method: "POST",
  });

  return parseResponse<GameState>(response);
}

export async function runSimulation(payload: {
  hands: number;
  player_a_strategy: StrategyName;
  player_b_strategy: StrategyName;
}): Promise<SimulationResult> {
  const response = await fetch(`${API_BASE_URL}/api/simulations/run`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  return parseResponse<SimulationResult>(response);
}

export async function fetchHistorySummary(): Promise<HistorySummary> {
  const response = await fetch(`${API_BASE_URL}/api/history/summary`);

  return parseResponse<HistorySummary>(response);
}
