import type { HistorySummary } from "../types/history";

export function HistoryPage({
  history,
  loading,
  onLoad,
}: {
  history: HistorySummary | null;
  loading: boolean;
  onLoad: () => void;
}) {
  return (
    <section className="history-page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Persistent Storage</p>
          <h1>Game History</h1>
          <p>
            Review saved game states, AI decisions, and simulation results from
            the database-backed persistence layer.
          </p>
        </div>

        <button onClick={onLoad} disabled={loading}>
          {loading ? "Loading..." : "Refresh History"}
        </button>
      </div>

      {history ? (
        <div className="history-grid">
          <div className="history-card">
            <h3>Saved Games</h3>

            {history.games.length === 0 ? (
              <p className="muted-text">No games saved yet.</p>
            ) : (
              history.games.map((game) => (
                <div className="history-row" key={game.id}>
                  <strong>{game.street}</strong>
                  <span>Pot ${game.pot}</span>
                  <small>{game.game_id.slice(0, 8)}</small>
                </div>
              ))
            )}
          </div>

          <div className="history-card">
            <h3>AI Decisions</h3>

            {history.ai_decisions.length === 0 ? (
              <p className="muted-text">No AI decisions saved yet.</p>
            ) : (
              history.ai_decisions.map((decision) => (
                <div className="history-row" key={decision.id}>
                  <strong>{decision.strategy.replace("_", " ")}</strong>
                  <span>{decision.action}</span>
                  <small>
                    {decision.confidence
                      ? `${Math.round(decision.confidence * 100)}% confidence`
                      : "n/a"}
                  </small>
                </div>
              ))
            )}
          </div>

          <div className="history-card">
            <h3>Simulation Runs</h3>

            {history.simulations.length === 0 ? (
              <p className="muted-text">No simulations saved yet.</p>
            ) : (
              history.simulations.map((simulation) => (
                <div className="history-row" key={simulation.id}>
                  <strong>{simulation.hands} hands</strong>
                  <span>
                    A {Math.round(simulation.player_a_win_rate * 100)}% · B{" "}
                    {Math.round(simulation.player_b_win_rate * 100)}%
                  </span>
                  <small>
                    {simulation.player_a_strategy.replace("_", " ")} vs{" "}
                    {simulation.player_b_strategy.replace("_", " ")}
                  </small>
                </div>
              ))
            )}
          </div>
        </div>
      ) : (
        <div className="empty-lab">
          <h2>No history loaded</h2>
          <p>Click Refresh History after playing hands or running simulations.</p>
        </div>
      )}
    </section>
  );
}
