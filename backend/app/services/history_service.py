from app.db.database import SessionLocal, init_db
from app.db.models import AiDecisionRecord, GameRecord, SimulationRunRecord


class HistoryService:
    def __init__(self):
        init_db()

    def save_game_state(self, state: dict):
        with SessionLocal() as session:
            record = GameRecord(
                game_id=state["game_id"],
                hand_number=state["hand_number"],
                street=state["street"],
                pot=state["pot"],
                state=state,
            )

            session.add(record)
            session.commit()

    def save_ai_decision(self, game_id: str, decision: dict):
        with SessionLocal() as session:
            record = AiDecisionRecord(
                game_id=game_id,
                strategy=decision.get("strategy", "unknown"),
                action=decision.get("action", "unknown"),
                amount=decision.get("amount"),
                confidence=decision.get("confidence"),
                payload=decision,
            )

            session.add(record)
            session.commit()

    def save_simulation(self, result: dict):
        with SessionLocal() as session:
            record = SimulationRunRecord(
                hands=result["hands"],
                player_a_strategy=result["player_a_strategy"],
                player_b_strategy=result["player_b_strategy"],
                player_a_win_rate=result["win_rates"]["player_a"],
                player_b_win_rate=result["win_rates"]["player_b"],
                tie_rate=result["win_rates"]["tie"],
                result=result,
            )

            session.add(record)
            session.commit()

    def latest_games(self, limit: int = 10) -> list[dict]:
        with SessionLocal() as session:
            records = (
                session.query(GameRecord)
                .order_by(GameRecord.id.desc())
                .limit(limit)
                .all()
            )

            return [self._game_to_dict(record) for record in records]

    def latest_ai_decisions(self, limit: int = 10) -> list[dict]:
        with SessionLocal() as session:
            records = (
                session.query(AiDecisionRecord)
                .order_by(AiDecisionRecord.id.desc())
                .limit(limit)
                .all()
            )

            return [self._decision_to_dict(record) for record in records]

    def latest_simulations(self, limit: int = 10) -> list[dict]:
        with SessionLocal() as session:
            records = (
                session.query(SimulationRunRecord)
                .order_by(SimulationRunRecord.id.desc())
                .limit(limit)
                .all()
            )

            return [self._simulation_to_dict(record) for record in records]

    def summary(self) -> dict:
        return {
            "games": self.latest_games(limit=8),
            "ai_decisions": self.latest_ai_decisions(limit=8),
            "simulations": self.latest_simulations(limit=8),
        }

    def _game_to_dict(self, record: GameRecord) -> dict:
        return {
            "id": record.id,
            "game_id": record.game_id,
            "hand_number": record.hand_number,
            "street": record.street,
            "pot": record.pot,
            "state": record.state,
            "created_at": record.created_at.isoformat() if record.created_at else None,
        }

    def _decision_to_dict(self, record: AiDecisionRecord) -> dict:
        return {
            "id": record.id,
            "game_id": record.game_id,
            "strategy": record.strategy,
            "action": record.action,
            "amount": record.amount,
            "confidence": record.confidence,
            "payload": record.payload,
            "created_at": record.created_at.isoformat() if record.created_at else None,
        }

    def _simulation_to_dict(self, record: SimulationRunRecord) -> dict:
        return {
            "id": record.id,
            "hands": record.hands,
            "player_a_strategy": record.player_a_strategy,
            "player_b_strategy": record.player_b_strategy,
            "player_a_win_rate": record.player_a_win_rate,
            "player_b_win_rate": record.player_b_win_rate,
            "tie_rate": record.tie_rate,
            "result": record.result,
            "created_at": record.created_at.isoformat() if record.created_at else None,
        }


history_service = HistoryService()
