from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.database import Base

class FunnelSessions(Base):
    __tablename__ = "funnel_sessions"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)