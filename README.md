# PokerMind Arena

PokerMind Arena is a full-stack AI-powered Texas Hold'em poker simulator built from scratch.
It includes a custom poker engine, interactive poker table UI, multiple AI strategies, simulation dashboard, persistent game history, and Docker-based setup.

The project is designed to demonstrate backend engineering, AI decision systems, game state management, simulation analytics, and modern full-stack development.

---

## Features

* Custom Texas Hold'em poker engine
* Card, deck, player, blinds, betting, and street logic
* Hand evaluator for all major poker hands
* Human vs AI gameplay
* Rule-based poker bot
* Monte Carlo equity bot
* MCTS-style decision engine
* AI decision explanation panel
* AI-vs-AI simulation dashboard
* Win rate and bankroll analytics
* Persistent history for games, AI decisions, and simulations
* Dynamic multi-page frontend
* Dockerized backend, frontend, and PostgreSQL setup

---

## Tech Stack

### Frontend

* React
* TypeScript
* Vite
* CSS
* Responsive multi-page UI

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* pytest

### AI / Algorithms

* Rule-based decision engine
* Monte Carlo equity simulation
* MCTS-style rollout engine
* Poker hand evaluation logic

### Database

* SQLite for local fallback
* PostgreSQL support through `DATABASE_URL`

### DevOps

* Docker
* Docker Compose
* Nginx frontend container
* PostgreSQL container

---

## Project Architecture

```text
React Frontend
│
├── Home Page
├── Play Arena
├── AI Lab
├── History Page
└── Architecture Page
        │
        ▼
FastAPI Backend
│
├── Game APIs
├── AI Action APIs
├── Simulation APIs
└── History APIs
        │
        ▼
Poker Engine
│
├── Card / Deck
├── Player State
├── Betting Logic
├── Street Flow
└── Hand Evaluator
        │
        ▼
AI Strategy Layer
│
├── Rule-Based Bot
├── Monte Carlo Bot
└── MCTS Bot
        │
        ▼
Persistence Layer
│
├── Game Records
├── AI Decision Records
└── Simulation Records
        │
        ▼
SQLite / PostgreSQL
```

---

## Pages

### Home Page

Landing page for the application with project overview, feature highlights, and navigation into the poker arena.

### Play Arena

Interactive poker table where the user can start a hand, make player actions, and allow different AI bots to act.

Supported player actions:

* Fold
* Check
* Call
* Raise

Supported AI strategies:

* Rule Bot
* Monte Carlo Bot
* MCTS Bot

### AI Lab

Simulation dashboard for comparing AI strategies across multiple hands.

It shows:

* Player A win rate
* Player B win rate
* Tie rate
* Final bankroll
* Bankroll trend
* Action distribution
* Recent hand outcomes

### History Page

Displays saved data from the persistence layer:

* Recent games
* AI decisions
* Simulation runs

### Architecture Page

Explains the high-level system design, backend modules, frontend pages, AI layer, and database flow.

---

## Backend Structure

```text
backend/
  app/
    ai/
      rule_based_bot.py
      monte_carlo_bot.py
      mcts_bot.py

    api/
      games.py
      simulations.py
      history.py
      health.py
      schemas.py

    core/
      card.py
      deck.py
      player.py
      game_state.py
      table.py
      hand_evaluator.py

    db/
      database.py
      models.py

    services/
      game_service.py
      simulation_service.py
      history_service.py

    tests/
      test_core_engine.py
      test_hand_evaluator.py
      test_game_api.py
      test_ai_api.py
      test_monte_carlo_bot.py
      test_mcts_bot.py
      test_simulation_api.py
      test_history_api.py

    main.py

  requirements.txt
  Dockerfile
```

---

## Frontend Structure

```text
frontend/
  src/
    components/
      Navigation.tsx
      PlayingCard.tsx
      PlayerPanel.tsx

    pages/
      HomePage.tsx
      PlayPage.tsx
      AiLabPage.tsx
      HistoryPage.tsx
      ArchitecturePage.tsx

    lib/
      api.ts

    types/
      game.ts
      simulation.ts
      history.ts

    App.tsx
    App.css
    main.tsx

  package.json
  Dockerfile
```

---

## API Endpoints

### Health

```text
GET /api/health
```

### Games

```text
POST /api/games
GET  /api/games/{game_id}
POST /api/games/{game_id}/action
POST /api/games/{game_id}/ai-action
POST /api/games/{game_id}/monte-carlo-action
POST /api/games/{game_id}/mcts-action
POST /api/games/{game_id}/next-street
POST /api/games/{game_id}/reset
```

### Simulations

```text
POST /api/simulations/run
```

### History

```text
GET /api/history/summary
GET /api/history/games
GET /api/history/ai-decisions
GET /api/history/simulations
```

---

## AI Strategies

### Rule-Based Bot

The rule-based bot uses simple poker heuristics.

It considers:

* Preflop card strength
* Pairs
* Suited cards
* Connected cards
* Current call amount
* Postflop hand category

This bot is fast and explainable.

---

### Monte Carlo Bot

The Monte Carlo bot estimates win probability by simulating possible remaining cards.

It considers:

* Player hole cards
* Known community cards
* Random opponent hands
* Random future board cards
* Repeated showdown comparisons

The bot returns:

* Action
* Confidence
* Equity percentage
* Simulation count
* Explanation

---

### MCTS Bot

The MCTS bot uses a Monte Carlo Tree Search style decision process.

It includes:

* Candidate action generation
* UCB-based selection
* Random rollout simulation
* Backpropagation
* Action value estimation
* Tree summary

The frontend displays MCTS reasoning with visits and average simulated value for each action.

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/pokermind-arena.git
cd pokermind-arena
```

---

## Backend Setup

```bash
cd backend

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

PYTHONPATH=. uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

Open a new terminal:

```bash
cd frontend

npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## Run Tests

From the backend folder:

```bash
cd backend
source .venv/bin/activate
PYTHONPATH=. pytest
```

---

## Docker Setup

Run the full project using Docker Compose:

```bash
docker compose up --build
```

Services:

```text
Frontend: http://localhost:3000
Backend:  http://localhost:8000
Docs:     http://localhost:8000/docs
Postgres: localhost:5432
```

Stop containers:

```bash
docker compose down
```

Remove database volume:

```bash
docker compose down -v
```

---

## Environment Variables

The backend supports this environment variable:

```text
DATABASE_URL
```

Example PostgreSQL URL:

```text
postgresql+psycopg://pokermind:pokermind@localhost:5432/pokermind
```

If `DATABASE_URL` is not provided, the backend uses local SQLite fallback.

---


## What I Built

This project was built from scratch as a full-stack AI poker simulator.

Main implementation work:

* Designed the poker domain models for cards, deck, players, and table state
* Built game state transitions for preflop, flop, turn, river, and showdown
* Implemented a Texas Hold'em hand evaluator
* Added FastAPI routes for game actions and AI decisions
* Created three AI strategies with explainable outputs
* Built AI-vs-AI simulation workflows
* Added persistent storage for games, AI decisions, and simulations
* Developed a dynamic React frontend with multiple pages
* Dockerized the full application with backend, frontend, and PostgreSQL



