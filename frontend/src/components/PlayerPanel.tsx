import { PlayingCard } from "./PlayingCard";
import type { Player } from "../types/game";

export function PlayerPanel({
  player,
  isCurrent,
  hideCards,
  position,
}: {
  player: Player;
  isCurrent: boolean;
  hideCards: boolean;
  position: "top" | "bottom";
}) {
  return (
    <div className={`player-panel ${isCurrent ? "active-player" : ""} ${position}`}>
      <div className="player-info">
        <p className="player-name">{player.name}</p>
        <p className="player-stack">${player.stack}</p>
      </div>

      <div className="hole-cards">
        {player.hole_cards.map((card, index) => (
          <PlayingCard
            key={`${card.display}-${index}`}
            card={card}
            hidden={hideCards}
            size="small"
          />
        ))}
      </div>

      <div className="player-meta">
        <span>Bet ${player.current_bet}</span>
        <span>Total ${player.total_committed}</span>
        {player.folded && <span className="danger">Folded</span>}
        {player.all_in && <span className="gold">All In</span>}
      </div>
    </div>
  );
}
