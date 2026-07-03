import "./App.css";

function App() {
  return (
    <main className="app-shell">
      <section className="hero">
        <div className="badge">Phase 0 Live</div>

        <h1>PokerMind Arena</h1>

        <p className="subtitle">
          An AI-powered Texas Hold&apos;em strategy simulator with a custom poker
          engine, intelligent bots, game replay, and analytics dashboard.
        </p>

        <div className="hero-actions">
          <button>Start Game</button>
          <button className="secondary">View AI Dashboard</button>
        </div>
      </section>

      <section className="table-preview">
        <div className="poker-table">
          <div className="player top-player">
            <span>AI Bot</span>
            <strong>$1,000</strong>
          </div>

          <div className="pot">Pot: $0</div>

          <div className="community-cards">
            <div className="card back"></div>
            <div className="card back"></div>
            <div className="card back"></div>
            <div className="card back"></div>
            <div className="card back"></div>
          </div>

          <div className="player bottom-player">
            <span>You</span>
            <strong>$1,000</strong>
          </div>
        </div>
      </section>
    </main>
  );
}

export default App;
