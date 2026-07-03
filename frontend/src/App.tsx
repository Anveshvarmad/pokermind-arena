import { useState } from "react";
import "./App.css";

import {
  applyAiAction,
  applyMctsAction,
  applyMonteCarloAction,
  applyPlayerAction,
  createGame,
  nextStreet,
  resetGame,
  runSimulation,
} from "./lib/api";
import type { Card, GameState, PokerAction, Player } from "./types/game";
import type { SimulationResult, StrategyName } from "./types/simulation";

function PlayingCard({ card, hidden = false }: { card?: Card; hidden?: boolean }) {
  if (hidden || !card) {
    return <div className="playing-card card-back" />;
  }

  const isRed = card.suit === "hearts" || card.suit === "diamonds";

  return (
    <div className={`playing-card ${isRed ? "red-card" : "black-card"}`}>
      <span>{card.rank}</span>
      <strong>{card.display.replace(card.rank, "")}</strong>
    </div>
  );
}

function PlayerPanel({
  player,
  isCurrent,
  hideCards,
}: {
  player: Player;
  isCurrent: boolean;
  hideCards: boolean;
}) {
  return (
    <div className={`player-panel ${isCurrent ? "active-player" : ""}`}>
      <div>
        <p className="player-name">{player.name}</p>
        <p className="player-stack">${player.stack}</p>
      </div>

      <div className="hole-cards">
        {player.hole_cards.map((card, index) => (
          <PlayingCard
            key={`${card.display}-${index}`}
            card={card}
            hidden={hideCards}
          />
        ))}
      </div>

      <div className="player-meta">
        <span>Bet: ${player.current_bet}</span>
        {player.folded && <span className="danger">Folded</span>}
        {player.all_in && <span className="gold">All In</span>}
      </div>
    </div>
  );
}

function StrategyLabel({ value }: { value: string }) {
  return <span>{value.replace("_", " ")}</span>;
}

function MiniBankrollChart({ result }: { result: SimulationResult }) {
  const points = result.bankroll_history.filter((_, index) => index % Math.max(1, Math.floor(result.bankroll_history.length / 28)) === 0);
  const minValue = Math.min(...points.map((point) => Math.min(point.player_a, point.player_b)));
  const maxValue = Math.max(...points.map((point) => Math.max(point.player_a, point.player_b)));
  const range = Math.max(1, maxValue - minValue);

  return (
    <div className="mini-chart">
      {points.map((point) => {
        const playerAHeight = 18 + ((point.player_a - minValue) / range) * 110;
        const playerBHeight = 18 + ((point.player_b - minValue) / range) * 110;

        return (
          <div className="chart-group" key={point.hand}>
            <div className="bar player-a-bar" style={{ height: `${playerAHeight}px` }} />
            <div className="bar player-b-bar" style={{ height: `${playerBHeight}px` }} />
          </div>
        );
      })}
    </div>
  );
}

function SimulationDashboard({
  result,
  hands,
  setHands,
  playerAStrategy,
  setPlayerAStrategy,
  playerBStrategy,
  setPlayerBStrategy,
  onRun,
  loading,
}: {
  result: SimulationResult | null;
  hands: number;
  setHands: (hands: number) => void;
  playerAStrategy: StrategyName;
  setPlayerAStrategy: (strategy: StrategyName) => void;
  playerBStrategy: StrategyName;
  setPlayerBStrategy: (strategy: StrategyName) => void;
  onRun: () => void;
  loading: boolean;
}) {
  const strategies: StrategyName[] = ["rule_based", "monte_carlo", "mcts"];

  return (
    <section className="simulation-section">
      <div className="section-heading">
        <div>
          <p className="eyebrow">AI Simulation Lab</p>
          <h2>Strategy Dashboard</h2>
          <p>
            Run AI-vs-AI hands and compare win rates, bankroll movement,
            actions, and recent outcomes.
          </p>
        </div>

        <div className="simulation-controls">
          <label>
            Hands
            <input
              type="number"
              min={1}
              max={1000}
              value={hands}
              onChange={(event) => setHands(Number(event.target.value))}
            />
          </label>

          <label>
            Player A
            <select
              value={playerAStrategy}
              onChange={(event) => setPlayerAStrategy(event.target.value as StrategyName)}
            >
              {strategies.map((strategy) => (
                <option key={strategy} value={strategy}>
                  {strategy.replace("_", " ")}
                </option>
              ))}
            </select>
          </label>

          <label>
            Player B
            <select
              value={playerBStrategy}
              onChange={(event) => setPlayerBStrategy(event.target.value as StrategyName)}
            >
              {strategies.map((strategy) => (
                <option key={strategy} value={strategy}>
                  {strategy.replace("_", " ")}
                </option>
              ))}
            </select>
          </label>

          <button onClick={onRun} disabled={loading}>
            Run Simulation
          </button>
        </div>
      </div>

      {result && (
        <div className="dashboard-grid">
          <div className="metric-card">
            <span>Player A</span>
            <strong>{Math.round(result.win_rates.player_a * 100)}%</strong>
            <p>
              <StrategyLabel value={result.player_a_strategy} /> · {result.wins.player_a} wins · ${result.final_bankroll.player_a}
            </p>
          </div>

          <div className="metric-card">
            <span>Player B</span>
            <strong>{Math.round(result.win_rates.player_b * 100)}%</strong>
            <p>
              <StrategyLabel value={result.player_b_strategy} /> · {result.wins.player_b} wins · ${result.final_bankroll.player_b}
            </p>
          </div>

          <div className="metric-card">
            <span>Ties</span>
            <strong>{Math.round(result.win_rates.tie * 100)}%</strong>
            <p>{result.wins.tie} tied hands out of {result.hands}</p>
          </div>

          <div className="chart-card">
            <h3>Bankroll Trend</h3>
            <MiniBankrollChart result={result} />
            <div className="legend">
              <span><b className="legend-a" /> Player A</span>
              <span><b className="legend-b" /> Player B</span>
            </div>
          </div>

          <div className="action-card">
            <h3>Action Distribution</h3>

            <div className="action-columns">
              <div>
                <h4>Player A</h4>
                {Object.entries(result.action_distribution.player_a).map(([action, count]) => (
                  <p key={action}>
                    <span>{action}</span>
                    <strong>{count}</strong>
                  </p>
                ))}
              </div>

              <div>
                <h4>Player B</h4>
                {Object.entries(result.action_distribution.player_b).map(([action, count]) => (
                  <p key={action}>
                    <span>{action}</span>
                    <strong>{count}</strong>
                  </p>
                ))}
              </div>
            </div>
          </div>

          <div className="recent-card">
            <h3>Recent Hands</h3>

            <div className="recent-list">
              {result.recent_hands.map((hand) => (
                <div className="recent-hand" key={hand.hand}>
                  <strong>Hand #{hand.hand}</strong>
                  <span>Winner: {hand.winner.replace("_", " ")}</span>
                  <span>A: {hand.player_a_best_hand.label}</span>
                  <span>B: {hand.player_b_best_hand.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

function App() {
  const [game, setGame] = useState<GameState | null>(null);
  const [raiseTo, setRaiseTo] = useState(60);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [simulationResult, setSimulationResult] = useState<SimulationResult | null>(null);
  const [simulationHands, setSimulationHands] = useState(100);
  const [playerAStrategy, setPlayerAStrategy] = useState<StrategyName>("rule_based");
  const [playerBStrategy, setPlayerBStrategy] = useState<StrategyName>("monte_carlo");
  const [simulationLoading, setSimulationLoading] = useState(false);

  async function runGameAction(action: () => Promise<GameState>) {
    try {
      setLoading(true);
      setError("");

      const updatedGame = await action();

      setGame(updatedGame);
      setRaiseTo(Math.max(updatedGame.highest_bet + updatedGame.big_blind, 40));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error");
    } finally {
      setLoading(false);
    }
  }

  async function handleRunSimulation() {
    try {
      setSimulationLoading(true);
      setError("");

      const result = await runSimulation({
        hands: simulationHands,
        player_a_strategy: playerAStrategy,
        player_b_strategy: playerBStrategy,
      });

      setSimulationResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Simulation failed");
    } finally {
      setSimulationLoading(false);
    }
  }

  function handleStartGame() {
    runGameAction(() => createGame());
  }

  function handleResetGame() {
    if (!game) return;

    runGameAction(() => resetGame(game.game_id));
  }

  function handleNextStreet() {
    if (!game) return;

    runGameAction(() => nextStreet(game.game_id));
  }

  function handleRuleBotAction() {
    if (!game) return;

    runGameAction(() => applyAiAction(game.game_id));
  }

  function handleMonteCarloAction() {
    if (!game) return;

    runGameAction(() => applyMonteCarloAction(game.game_id));
  }

  function handleMctsAction() {
    if (!game) return;

    runGameAction(() => applyMctsAction(game.game_id));
  }

  function handlePlayerAction(action: PokerAction) {
    if (!game) return;

    runGameAction(() =>
      applyPlayerAction(game.game_id, {
        player_index: game.current_player_index,
        action,
        amount: action === "raise" ? raiseTo : undefined,
      }),
    );
  }

  const currentPlayer = game?.players[game.current_player_index];
  const isAiTurn =
    currentPlayer?.name.toLowerCase().includes("ai") ||
    currentPlayer?.name.toLowerCase().includes("bot");

  const canMoveStreet =
    game &&
    game.street !== "waiting" &&
    game.street !== "showdown" &&
    !game.hand_complete;

  return (
    <main className="page">
      <section className="hero-section">
        <div>
          <p className="eyebrow">AI Poker Simulator</p>
          <h1>PokerMind Arena</h1>
          <p className="subtitle">
            Play through Texas Hold&apos;em hands and compare rule-based,
            Monte Carlo, and MCTS poker strategies.
          </p>
        </div>

        <div className="hero-buttons">
          <button onClick={handleStartGame} disabled={loading}>
            {game ? "New Game" : "Start Game"}
          </button>

          {game && (
            <button className="secondary-button" onClick={handleResetGame} disabled={loading}>
              Reset Hand
            </button>
          )}
        </div>
      </section>

      {error && <div className="error-box">{error}</div>}

      <section className="game-layout">
        <div className="table-card">
          <div className="stats-strip">
            <div>
              <span>Street</span>
              <strong>{game?.street ?? "not started"}</strong>
            </div>

            <div>
              <span>Pot</span>
              <strong>${game?.pot ?? 0}</strong>
            </div>

            <div>
              <span>To Call</span>
              <strong>${game?.call_amount ?? 0}</strong>
            </div>

            <div>
              <span>Deck</span>
              <strong>{game?.deck_remaining ?? 52}</strong>
            </div>
          </div>

          <div className="poker-table">
            {game ? (
              <>
                <div className="seat top-seat">
                  <PlayerPanel
                    player={game.players[1]}
                    isCurrent={game.current_player_index === 1}
                    hideCards={game.street !== "showdown"}
                  />
                </div>

                <div className="center-board">
                  <div className="pot-chip">Pot ${game.pot}</div>

                  <div className="community-row">
                    {[0, 1, 2, 3, 4].map((index) => (
                      <PlayingCard
                        key={index}
                        card={game.community_cards[index]}
                        hidden={!game.community_cards[index]}
                      />
                    ))}
                  </div>
                </div>

                <div className="seat bottom-seat">
                  <PlayerPanel
                    player={game.players[0]}
                    isCurrent={game.current_player_index === 0}
                    hideCards={false}
                  />
                </div>
              </>
            ) : (
              <div className="empty-state">
                <h2>No hand started yet</h2>
                <p>Click Start Game to deal hole cards and post blinds.</p>
              </div>
            )}
          </div>
        </div>

        <aside className="control-panel">
          <div className="panel-block">
            <h2>Game Controls</h2>

            {game ? (
              <>
                <p className="turn-label">
                  Current Turn: <strong>{currentPlayer?.name}</strong>
                </p>

                {isAiTurn ? (
                  <div className="ai-turn-box">
                    <p>Choose which AI strategy should act for the bot.</p>

                    <div className="bot-action-grid">
                      <button disabled={loading} onClick={handleRuleBotAction}>
                        Rule Bot Act
                      </button>

                      <button disabled={loading} onClick={handleMonteCarloAction}>
                        Monte Carlo Bot Act
                      </button>

                      <button disabled={loading} onClick={handleMctsAction}>
                        MCTS Bot Act
                      </button>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="action-grid">
                      <button
                        className="danger-button"
                        disabled={loading || !game.available_actions.includes("fold")}
                        onClick={() => handlePlayerAction("fold")}
                      >
                        Fold
                      </button>

                      <button
                        disabled={loading || !game.available_actions.includes("check")}
                        onClick={() => handlePlayerAction("check")}
                      >
                        Check
                      </button>

                      <button
                        disabled={loading || !game.available_actions.includes("call")}
                        onClick={() => handlePlayerAction("call")}
                      >
                        Call ${game.call_amount}
                      </button>
                    </div>

                    <div className="raise-box">
                      <label htmlFor="raiseTo">Raise To</label>
                      <input
                        id="raiseTo"
                        type="number"
                        min={game.highest_bet + game.big_blind}
                        value={raiseTo}
                        onChange={(event) => setRaiseTo(Number(event.target.value))}
                      />
                      <button
                        disabled={loading || !game.available_actions.includes("raise")}
                        onClick={() => handlePlayerAction("raise")}
                      >
                        Raise
                      </button>
                    </div>
                  </>
                )}

                <button
                  className="wide-button secondary-button"
                  disabled={loading || !canMoveStreet}
                  onClick={handleNextStreet}
                >
                  Deal Next Street
                </button>
              </>
            ) : (
              <p className="muted-text">
                Start a game to unlock poker actions.
              </p>
            )}
          </div>

          {game?.ai_decision && (
            <div className="panel-block ai-decision-card">
              <h2>AI Decision</h2>

              <div className="decision-row">
                <span>Strategy</span>
                <strong>{game.ai_decision.strategy?.replace("_", " ") ?? "rule based"}</strong>
              </div>

              <div className="decision-row">
                <span>Action</span>
                <strong>{game.ai_decision.action}</strong>
              </div>

              <div className="decision-row">
                <span>Confidence</span>
                <strong>{Math.round(game.ai_decision.confidence * 100)}%</strong>
              </div>

              {typeof game.ai_decision.equity === "number" && (
                <div className="decision-row">
                  <span>Equity</span>
                  <strong>{Math.round(game.ai_decision.equity * 100)}%</strong>
                </div>
              )}

              {typeof game.ai_decision.estimated_value === "number" && (
                <div className="decision-row">
                  <span>MCTS Value</span>
                  <strong>{game.ai_decision.estimated_value}</strong>
                </div>
              )}

              {game.ai_decision.simulations && (
                <div className="decision-row">
                  <span>Simulations</span>
                  <strong>{game.ai_decision.simulations}</strong>
                </div>
              )}

              {game.ai_decision.iterations && (
                <div className="decision-row">
                  <span>Iterations</span>
                  <strong>{game.ai_decision.iterations}</strong>
                </div>
              )}

              <p>{game.ai_decision.reason}</p>

              {game.ai_decision.tree_summary && (
                <div className="tree-summary">
                  <h3>MCTS Tree Summary</h3>

                  {game.ai_decision.tree_summary.map((item, index) => (
                    <div className="tree-row" key={`${item.action}-${index}`}>
                      <span>
                        {item.action}
                        {item.amount ? ` $${item.amount}` : ""}
                      </span>
                      <span>{item.visits} visits</span>
                      <strong>{item.average_value}</strong>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          <div className="panel-block">
            <h2>Current State</h2>

            {game ? (
              <pre>{JSON.stringify(game, null, 2)}</pre>
            ) : (
              <p className="muted-text">Game state will appear here.</p>
            )}
          </div>
        </aside>
      </section>

      <SimulationDashboard
        result={simulationResult}
        hands={simulationHands}
        setHands={setSimulationHands}
        playerAStrategy={playerAStrategy}
        setPlayerAStrategy={setPlayerAStrategy}
        playerBStrategy={playerBStrategy}
        setPlayerBStrategy={setPlayerBStrategy}
        onRun={handleRunSimulation}
        loading={simulationLoading}
      />
    </main>
  );
}

export default App;
