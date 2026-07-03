export type HistoryGame = {
  id: number;
  game_id: string;
  hand_number: number;
  street: string;
  pot: number;
  created_at: string | null;
};

export type HistoryAiDecision = {
  id: number;
  game_id: string;
  strategy: string;
  action: string;
  amount: number | null;
  confidence: number | null;
  created_at: string | null;
};

export type HistorySimulation = {
  id: number;
  hands: number;
  player_a_strategy: string;
  player_b_strategy: string;
  player_a_win_rate: number;
  player_b_win_rate: number;
  tie_rate: number;
  created_at: string | null;
};

export type HistorySummary = {
  games: HistoryGame[];
  ai_decisions: HistoryAiDecision[];
  simulations: HistorySimulation[];
};
