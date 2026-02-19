from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.db import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__="user"
    id=Column(Integer, primary_key=True)
    username=Column(String, unique=True, nullable=False)
    name=Column(String, nullable=False)
    email=Column(String, unique=True)
    password=Column(String)

class Game(Base):
    __tablename__="table"
    __table_args__ = (
        CheckConstraint('start_time < end_time'),
        CheckConstraint('host != winner')
    )
    id=Column(Integer, primary_key=True)
    host=Column(Integer, ForeignKey("user.id"))
    description=Column(Text, nullable=False)
    start_time=Column(DateTime, default=lambda: datetime.now(timezone.utc))
    end_time=Column(DateTime, nullable=False)
    winner=Column(Integer, ForeignKey("Uuser.id"))

class Bingo(Base):
    __tablename__="bingo"
    id=Column(Integer, primary_key=True)
    row=Column(Integer, nullable=False)
    col=Column(Integer, nullable=False)
    bingo_char=Column(String, nullable=False)
    image_link=Column(String, unique=True)

class GameUserBingo(Base):
    __tablename__ = "game_user_bingo"

    game_id = Column(ForeignKey("game.id"), primary_key=True)
    user_id = Column(ForeignKey("user.id"), primary_key=True)
    bingo_id = Column(ForeignKey("bingo.id"), primary_key=True)

    game = relationship("game", back_populates="game_user_bingos")
    user = relationship("user", back_populates="game_user_bingos")
    bingo = relationship("bingo", back_populates="game_user_bingos")
