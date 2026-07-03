import { useState } from "react";
import "./App.css";

import {
  applyAiAction,
  applyPlayerAction,
  createGame,
  nextStreet,
  resetGame,
} from "./lib/api";
import type { Card, GameState, PokerAction, Player } from "./types/game";

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

function App() {
  const [game, setGame] = useState<GameState | null>(null);
  const [raiseTo, setRaiseTo] = useState(60);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function runAction(action: () => Promise<GameState>) {
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

  function handleStartGame() {
    runAction(() => createGame());
  }

  function handleResetGame() {
    if (!game) return;

    runAction(() => resetGame(game.game_id));
  }

  function handleNextStreet() {
    if (!game) return;

    runAction(() => nextStreet(game.game_id));
  }

  function handleAiAction() {
    if (!game) return;

    runAction(() => applyAiAction(game.game_id));
  }

  function handlePlayerAction(action: PokerAction) {
    if (!game) return;

    runAction(() =>
      applyPlayerAction(game.game_id, {
        player_index: game.current_player_index,
        action,
        amount: action === "raise" ? raiseTo : undefined,
      }),
    );
  }

  const currentPlayer = game?.players[game.current_player_index];
  const isAiTurn = currentPlayer?.name.toLowerCase().includes("ai") || currentPlayer?.name.toLowerCase().includes("bot");

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
            Play through a Texas Hold&apos;em hand, inspect each state transition,
            and let a rule-based AI bot make explainable poker decisions.
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
                    <p>The AI bot is waiting to act.</p>
                    <button className="wide-button" disabled={loading} onClick={handleAiAction}>
                      Let AI Act
                    </button>
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
                <span>Action</span>
                <strong>{game.ai_decision.action}</strong>
              </div>
              <div className="decision-row">
                <span>Confidence</span>
                <strong>{Math.round(game.ai_decision.confidence * 100)}%</strong>
              </div>
              <p>{game.ai_decision.reason}</p>
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
    </main>
  );
}

export default App;
