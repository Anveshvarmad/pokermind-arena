import type { Card } from "../types/game";

export function PlayingCard({
  card,
  hidden = false,
  size = "normal",
}: {
  card?: Card;
  hidden?: boolean;
  size?: "small" | "normal" | "large";
}) {
  if (hidden || !card) {
    return <div className={`playing-card card-back ${size}`} />;
  }

  const isRed = card.suit === "hearts" || card.suit === "diamonds";
  const suitSymbol = card.display.replace(card.rank, "");

  return (
    <div className={`playing-card ${isRed ? "red-card" : "black-card"} ${size}`}>
      <span>{card.rank}</span>
      <strong>{suitSymbol}</strong>
    </div>
  );
}
