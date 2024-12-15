from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

class FunnelSessions(Base):
    __tablename__ = "funnel_sessions"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class FunnelCourses(Base):
    __tablename__ = "funnel_courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    hill = Column(String, nullable=False)
    img = Column(String, nullable=False)

class FunnelRegistrations(Base):
    __tablename__ = "funnel_registrations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('funnel_sessions.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('funnel_courses.id'), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    children_count = Column(Integer, nullable=False)
    adults_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    course = relationship("FunnelCourses", foreign_keys=[course_id])
    session = relationship("FunnelSessions", foreign_keys=[session_id])