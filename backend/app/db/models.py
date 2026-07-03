from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, func

from app.db.database import Base


class GameRecord(Base):
    __tablename__ = "game_records"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(String, index=True, nullable=False)
    hand_number = Column(Integer, nullable=False)
    street = Column(String, nullable=False)
    pot = Column(Integer, nullable=False)
    state = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AiDecisionRecord(Base):
    __tablename__ = "ai_decision_records"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(String, index=True, nullable=False)
    strategy = Column(String, nullable=False)
    action = Column(String, nullable=False)
    amount = Column(Integer, nullable=True)
    confidence = Column(Float, nullable=True)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulationRunRecord(Base):
    __tablename__ = "simulation_run_records"

    id = Column(Integer, primary_key=True, index=True)
    hands = Column(Integer, nullable=False)
    player_a_strategy = Column(String, nullable=False)
    player_b_strategy = Column(String, nullable=False)
    player_a_win_rate = Column(Float, nullable=False)
    player_b_win_rate = Column(Float, nullable=False)
    tie_rate = Column(Float, nullable=False)
    result = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
