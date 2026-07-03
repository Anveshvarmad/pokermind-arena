import type { PageName } from "../components/Navigation";

export function HomePage({
  onStart,
  onNavigate,
}: {
  onStart: () => void;
  onNavigate: (page: PageName) => void;
}) {
  function startGame() {
    onStart();
    onNavigate("play");
  }

  return (
    <section className="home-page">
      <div className="hero-grid">
        <div className="hero-copy">
          <p className="eyebrow">AI Poker Strategy Simulator</p>
          <h1>
            Play poker against
            <span> intelligent agents.</span>
          </h1>
          <p className="subtitle">
            PokerMind Arena is a Texas Hold&apos;em simulator with a custom game
            engine, rule-based AI, Monte Carlo equity search, MCTS reasoning,
            simulations, and persistent analytics.
          </p>

          <div className="hero-actions">
            <button onClick={startGame}>Enter Poker Arena</button>
            <button className="secondary-button" onClick={() => onNavigate("lab")}>
              Open AI Lab
            </button>
          </div>

          <div className="feature-strip">
            <div>
              <strong>3</strong>
              <span>AI strategies</span>
            </div>
            <div>
              <strong>5</strong>
              <span>dynamic pages</span>
            </div>
            <div>
              <strong>1000+</strong>
              <span>simulated hands</span>
            </div>
          </div>
        </div>

        <div className="casino-preview">
          <div className="floating-card card-one">A♠</div>
          <div className="floating-card card-two">K♥</div>
          <div className="table-orbit">
            <div className="table-glow" />
            <div className="preview-table">
              <div className="preview-seat top">AI Bot</div>
              <div className="preview-board">
                <span>Q♠</span>
                <span>J♠</span>
                <span>10♠</span>
                <span>?</span>
                <span>?</span>
              </div>
              <div className="preview-pot">$240 POT</div>
              <div className="preview-seat bottom">You</div>
            </div>
          </div>
        </div>
      </div>

      <div className="home-cards">
        <article>
          <h3>Real Poker Engine</h3>
          <p>Cards, deck, blinds, streets, betting actions, hand evaluator, and winner detection are built from scratch.</p>
        </article>

        <article>
          <h3>AI Decision Layer</h3>
          <p>Compare rule-based logic, Monte Carlo equity estimation, and MCTS-style simulated rollouts.</p>
        </article>

        <article>
          <h3>Analytics Dashboard</h3>
          <p>Run AI-vs-AI simulations and track win rates, bankroll trend, action spread, and recent outcomes.</p>
        </article>
      </div>
    </section>
  );
}
