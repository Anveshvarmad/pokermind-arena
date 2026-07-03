export function ArchitecturePage() {
  return (
    <section className="architecture-page">
      <div className="page-header">
        <div>
          <p className="eyebrow">System Design</p>
          <h1>Architecture</h1>
          <p>
            PokerMind Arena is built as a full-stack AI simulation platform with
            a custom poker engine, FastAPI backend, strategy layer, persistence,
            and a dynamic React frontend.
          </p>
        </div>
      </div>

      <div className="architecture-map">
        <div className="arch-node frontend">
          <span>Frontend</span>
          <strong>React + TypeScript</strong>
          <p>Multi-page game UI, poker table, AI lab, history, and architecture views.</p>
        </div>

        <div className="arch-line" />

        <div className="arch-node api">
          <span>Backend API</span>
          <strong>FastAPI</strong>
          <p>Game APIs, AI action endpoints, simulation APIs, and history routes.</p>
        </div>

        <div className="arch-line" />

        <div className="arch-node engine">
          <span>Poker Engine</span>
          <strong>Custom Python Core</strong>
          <p>Cards, deck, players, streets, betting state, hand evaluator, and winner logic.</p>
        </div>

        <div className="arch-line" />

        <div className="arch-node ai">
          <span>AI Layer</span>
          <strong>Rule Bot · Monte Carlo · MCTS</strong>
          <p>Explainable decision engines with equity, confidence, rollouts, and tree summary.</p>
        </div>

        <div className="arch-line" />

        <div className="arch-node database">
          <span>Persistence</span>
          <strong>SQLAlchemy + PostgreSQL</strong>
          <p>Stores games, AI decisions, simulation runs, and analytics history.</p>
        </div>
      </div>

      <div className="tech-grid">
        <article>
          <h3>Backend</h3>
          <p>Python, FastAPI, Pydantic, SQLAlchemy, pytest</p>
        </article>

        <article>
          <h3>Frontend</h3>
          <p>React, TypeScript, Vite, dynamic CSS, responsive UI</p>
        </article>

        <article>
          <h3>AI</h3>
          <p>Rule-based decision logic, Monte Carlo equity estimation, MCTS rollouts</p>
        </article>

        <article>
          <h3>DevOps</h3>
          <p>Docker Compose, PostgreSQL container, backend container, frontend container</p>
        </article>
      </div>
    </section>
  );
}
