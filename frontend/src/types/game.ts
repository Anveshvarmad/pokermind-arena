export type PokerAction = "fold" | "check" | "call" | "raise";

export type Card = {
  rank: string;
  suit: string;
  value: number;
  display: string;
};

export type Player = {
  id: string;
  name: string;
  stack: number;
  current_bet: number;
  total_committed: number;
  folded: boolean;
  all_in: boolean;
  hole_cards: Card[];
};

export type MctsTreeItem = {
  action: PokerAction;
  amount: number | null;
  visits: number;
  average_value: number;
};

export type AiDecision = {
  strategy?: "rule_based" | "monte_carlo" | "mcts";
  action: PokerAction;
  amount: number | null;
  confidence: number;
  reason: string;
  equity?: number;
  simulations?: number;
  estimated_value?: number;
  iterations?: number;
  tree_summary?: MctsTreeItem[];
};

export type GameState = {
  game_id: string;
  hand_number: number;
  street: string;
  dealer_index: number;
  current_player_index: number;
  current_player_id: string;
  current_player_name: string;
  pot: number;
  small_blind: number;
  big_blind: number;
  highest_bet: number;
  call_amount: number;
  available_actions: PokerAction[];
  hand_complete: boolean;
  deck_remaining: number;
  community_cards: Card[];
  players: Player[];
  ai_decision?: AiDecision;
};

export type PlayerActionPayload = {
  player_index: number;
  action: PokerAction;
  amount?: number;
};
