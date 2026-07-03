export type StrategyName = "rule_based" | "monte_carlo" | "mcts";

export type BankrollPoint = {
  hand: number;
  player_a: number;
  player_b: number;
};

export type SimulationCard = {
  rank: string;
  suit: string;
  value: number;
  display: string;
};

export type RecentHand = {
  hand: number;
  winner: "player_a" | "player_b" | "tie";
  player_a_cards: SimulationCard[];
  player_b_cards: SimulationCard[];
  community_cards: SimulationCard[];
  player_a_best_hand: {
    label: string;
  };
  player_b_best_hand: {
    label: string;
  };
  bankroll_after: {
    player_a: number;
    player_b: number;
  };
};

export type SimulationResult = {
  hands: number;
  player_a_strategy: StrategyName;
  player_b_strategy: StrategyName;
  wins: {
    player_a: number;
    player_b: number;
    tie: number;
  };
  win_rates: {
    player_a: number;
    player_b: number;
    tie: number;
  };
  final_bankroll: {
    player_a: number;
    player_b: number;
  };
  bankroll_history: BankrollPoint[];
  action_distribution: {
    player_a: Record<string, number>;
    player_b: Record<string, number>;
  };
  recent_hands: RecentHand[];
};
