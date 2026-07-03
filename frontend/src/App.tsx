import { useState } from "react";
import "./App.css";

import { Navigation, type PageName } from "./components/Navigation";
import {
  applyAiAction,
  applyMctsAction,
  applyMonteCarloAction,
  applyPlayerAction,
  createGame,
  fetchHistorySummary,
  nextStreet,
  resetGame,
  runSimulation,
} from "./lib/api";
import { AiLabPage } from "./pages/AiLabPage";
import { ArchitecturePage } from "./pages/ArchitecturePage";
import { HistoryPage } from "./pages/HistoryPage";
import { HomePage } from "./pages/HomePage";
import { PlayPage } from "./pages/PlayPage";
import type { GameState, PokerAction } from "./types/game";
import type { HistorySummary } from "./types/history";
import type { SimulationResult, StrategyName } from "./types/simulation";

function App() {
  const [activePage, setActivePage] = useState<PageName>("home");
  const [game, setGame] = useState<GameState | null>(null);
  const [raiseTo, setRaiseTo] = useState(60);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [simulationResult, setSimulationResult] = useState<SimulationResult | null>(null);
  const [simulationHands, setSimulationHands] = useState(100);
  const [playerAStrategy, setPlayerAStrategy] = useState<StrategyName>("rule_based");
  const [playerBStrategy, setPlayerBStrategy] = useState<StrategyName>("monte_carlo");
  const [simulationLoading, setSimulationLoading] = useState(false);

  const [history, setHistory] = useState<HistorySummary | null>(null);
  const [historyLoading, setHistoryLoading] = useState(false);

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

  async function handleLoadHistory() {
    try {
      setHistoryLoading(true);
      setError("");

      const result = await fetchHistorySummary();

      setHistory(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load history");
    } finally {
      setHistoryLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <div className="background-grid" />
      <div className="orb orb-one" />
      <div className="orb orb-two" />

      <Navigation activePage={activePage} onNavigate={setActivePage} />

      {error && <div className="error-box">{error}</div>}

      {activePage === "home" && (
        <HomePage onStart={handleStartGame} onNavigate={setActivePage} />
      )}

      {activePage === "play" && (
        <PlayPage
          game={game}
          loading={loading}
          raiseTo={raiseTo}
          setRaiseTo={setRaiseTo}
          onStartGame={handleStartGame}
          onResetGame={handleResetGame}
          onNextStreet={handleNextStreet}
          onRuleBotAction={handleRuleBotAction}
          onMonteCarloAction={handleMonteCarloAction}
          onMctsAction={handleMctsAction}
          onPlayerAction={handlePlayerAction}
        />
      )}

      {activePage === "lab" && (
        <AiLabPage
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
      )}

      {activePage === "history" && (
        <HistoryPage
          history={history}
          loading={historyLoading}
          onLoad={handleLoadHistory}
        />
      )}

      {activePage === "architecture" && <ArchitecturePage />}
    </main>
  );
}

export default App;
