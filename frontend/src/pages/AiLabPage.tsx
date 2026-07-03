import type { SimulationResult, StrategyName } from "../types/simulation";

function StrategyLabel({ value }: { value: string }) {
  return <span>{value.replace("_", " ")}</span>;
}

function MiniBankrollChart({ result }: { result: SimulationResult }) {
  const step = Math.max(1, Math.floor(result.bankroll_history.length / 32));
  const points = result.bankroll_history.filter((_, index) => index % step === 0);
  const minValue = Math.min(...points.map((point) => Math.min(point.player_a, point.player_b)));
  const maxValue = Math.max(...points.map((point) => Math.max(point.player_a, point.player_b)));
  const range = Math.max(1, maxValue - minValue);

  return (
    <div className="mini-chart">
      {points.map((point) => {
        const playerAHeight = 18 + ((point.player_a - minValue) / range) * 120;
        const playerBHeight = 18 + ((point.player_b - minValue) / range) * 120;

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

export function AiLabPage({
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
    <section className="ai-lab-page">
      <div className="page-header">
        <div>
          <p className="eyebrow">AI Simulation Lab</p>
          <h1>Strategy Dashboard</h1>
          <p>
            Run AI-vs-AI matches and compare win rates, bankroll movement,
            action distribution, and recent hand outcomes.
          </p>
        </div>
      </div>

      <div className="simulation-console">
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
          {loading ? "Running..." : "Run Simulation"}
        </button>
      </div>

      {result ? (
        <div className="dashboard-grid">
          <div className="metric-card glow-card">
            <span>Player A Win Rate</span>
            <strong>{Math.round(result.win_rates.player_a * 100)}%</strong>
            <p>
              <StrategyLabel value={result.player_a_strategy} /> · {result.wins.player_a} wins · ${result.final_bankroll.player_a}
            </p>
          </div>

          <div className="metric-card glow-card purple">
            <span>Player B Win Rate</span>
            <strong>{Math.round(result.win_rates.player_b * 100)}%</strong>
            <p>
              <StrategyLabel value={result.player_b_strategy} /> · {result.wins.player_b} wins · ${result.final_bankroll.player_b}
            </p>
          </div>

          <div className="metric-card glow-card gold-card">
            <span>Tie Rate</span>
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
      ) : (
        <div className="empty-lab">
          <h2>No simulation yet</h2>
          <p>Select two strategies and run a match to generate analytics.</p>
        </div>
      )}
    </section>
  );
}
