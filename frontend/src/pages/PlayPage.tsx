import { PlayerPanel } from "../components/PlayerPanel";
import { PlayingCard } from "../components/PlayingCard";
import type { GameState, PokerAction } from "../types/game";

export function PlayPage({
  game,
  loading,
  raiseTo,
  setRaiseTo,
  onStartGame,
  onResetGame,
  onNextStreet,
  onRuleBotAction,
  onMonteCarloAction,
  onMctsAction,
  onPlayerAction,
}: {
  game: GameState | null;
  loading: boolean;
  raiseTo: number;
  setRaiseTo: (value: number) => void;
  onStartGame: () => void;
  onResetGame: () => void;
  onNextStreet: () => void;
  onRuleBotAction: () => void;
  onMonteCarloAction: () => void;
  onMctsAction: () => void;
  onPlayerAction: (action: PokerAction) => void;
}) {
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
    <section className="play-page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Live Poker Arena</p>
          <h1>Texas Hold&apos;em Table</h1>
          <p>
            Play a hand, inspect the state, and choose which AI strategy acts for
            the bot.
          </p>
        </div>

        <div className="page-actions">
          <button onClick={onStartGame} disabled={loading}>
            {game ? "New Game" : "Start Game"}
          </button>

          {game && (
            <button className="secondary-button" onClick={onResetGame} disabled={loading}>
              Reset Hand
            </button>
          )}
        </div>
      </div>

      <div className="arena-layout">
        <div className="main-table-shell">
          <div className="stats-ribbon">
            <div>
              <span>Street</span>
              <strong>{game?.street ?? "waiting"}</strong>
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

          <div className="real-table">
            <div className="felt-lines" />

            {game ? (
              <>
                <div className="dealer-button">D</div>

                <div className="seat top-seat">
                  <PlayerPanel
                    player={game.players[1]}
                    isCurrent={game.current_player_index === 1}
                    hideCards={game.street !== "showdown"}
                    position="top"
                  />
                </div>

                <div className="center-board">
                  <div className="chip-stack">
                    <span />
                    <span />
                    <span />
                  </div>

                  <div className="pot-chip">POT ${game.pot}</div>

                  <div className="community-row">
                    {[0, 1, 2, 3, 4].map((index) => (
                      <PlayingCard
                        key={index}
                        card={game.community_cards[index]}
                        hidden={!game.community_cards[index]}
                        size="large"
                      />
                    ))}
                  </div>
                </div>

                <div className="seat bottom-seat">
                  <PlayerPanel
                    player={game.players[0]}
                    isCurrent={game.current_player_index === 0}
                    hideCards={false}
                    position="bottom"
                  />
                </div>
              </>
            ) : (
              <div className="empty-table-state">
                <h2>Waiting for players</h2>
                <p>Start a game to deal cards and post blinds.</p>
                <button onClick={onStartGame}>Deal Cards</button>
              </div>
            )}
          </div>
        </div>

        <aside className="game-sidebar">
          <div className="glass-panel">
            <h2>Controls</h2>

            {game ? (
              <>
                <p className="turn-label">
                  Current Turn: <strong>{currentPlayer?.name}</strong>
                </p>

                {isAiTurn ? (
                  <div className="ai-turn-box">
                    <p>Choose an AI strategy for this decision.</p>

                    <div className="bot-action-grid">
                      <button disabled={loading} onClick={onRuleBotAction}>
                        Rule Bot
                      </button>
                      <button disabled={loading} onClick={onMonteCarloAction}>
                        Monte Carlo
                      </button>
                      <button disabled={loading} onClick={onMctsAction}>
                        MCTS
                      </button>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="action-grid">
                      <button
                        className="danger-button"
                        disabled={loading || !game.available_actions.includes("fold")}
                        onClick={() => onPlayerAction("fold")}
                      >
                        Fold
                      </button>

                      <button
                        disabled={loading || !game.available_actions.includes("check")}
                        onClick={() => onPlayerAction("check")}
                      >
                        Check
                      </button>

                      <button
                        disabled={loading || !game.available_actions.includes("call")}
                        onClick={() => onPlayerAction("call")}
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
                        onClick={() => onPlayerAction("raise")}
                      >
                        Raise
                      </button>
                    </div>
                  </>
                )}

                <button
                  className="wide-button secondary-button"
                  disabled={loading || !canMoveStreet}
                  onClick={onNextStreet}
                >
                  Deal Next Street
                </button>
              </>
            ) : (
              <p className="muted-text">Start a game to unlock actions.</p>
            )}
          </div>

          {game?.ai_decision && (
            <div className="glass-panel ai-decision-card">
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

              {game.ai_decision.iterations && (
                <div className="decision-row">
                  <span>Iterations</span>
                  <strong>{game.ai_decision.iterations}</strong>
                </div>
              )}

              {game.ai_decision.simulations && (
                <div className="decision-row">
                  <span>Simulations</span>
                  <strong>{game.ai_decision.simulations}</strong>
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

          <div className="glass-panel">
            <h2>Current State</h2>
            {game ? <pre>{JSON.stringify(game, null, 2)}</pre> : <p className="muted-text">No game state yet.</p>}
          </div>
        </aside>
      </div>
    </section>
  );
}
