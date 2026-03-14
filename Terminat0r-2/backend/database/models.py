from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(128), unique=True, nullable=False, index=True)
    gold = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    quests = relationship("Quest", back_populates="user")


class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prompt = Column(Text, nullable=False)
    generated_json = Column(Text, nullable=True)
    status = Column(String(32), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quests")


class EventLog(Base):
    __tablename__ = "events_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False, index=True)
    event_type = Column(String(64), nullable=False)
    event_name = Column(String(128), nullable=True)
    payload = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserSkin(Base):
    """Скіни маскота, що належать користувачу."""
    __tablename__ = "user_skins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(128), nullable=False, index=True)
    skin_id = Column(Integer, nullable=False)
    source = Column(String(32), default="wheel")  # wheel | purchase | starter
    created_at = Column(DateTime, default=datetime.utcnow)


class RoutineCompletion(Base):
    """Виконання щоденної/тижневої справи та отримання бонусу за всі 5."""
    __tablename__ = "routine_completions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(128), nullable=False, index=True)
    routine_id = Column(String(64), nullable=False)
    frequency = Column(String(16), nullable=False)  # daily | weekly
    period_key = Column(String(32), nullable=False)  # YYYY-MM-DD | YYYY-Wnn
    reward_claimed = Column(Integer, default=0)  # 0=тільки справу, 1=бонус за всі 5
    created_at = Column(DateTime, default=datetime.utcnow)
