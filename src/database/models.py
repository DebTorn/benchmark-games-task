from typing import List
from typing import Optional
from datetime import datetime, timezone
import decimal
from src.config.enums.report_link_enums import TypeEnum
from src.config.enums.user_warning_enums import LevelEnum, CategoryEnum

from sqlalchemy import ForeignKey, String, DateTime, text, Integer, JSON, Enum, DECIMAL, Text, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

"""
    REPORT
"""

class Player(Base):
    __tablename__ = 'players'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    
class Aggregator(Base):
    __tablename__ = 'aggregators'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    
class Report(Base):
    __tablename__ = 'reports'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    aggregator_id: Mapped[int] = mapped_column(Integer, ForeignKey("aggregators.id"))
    valid: Mapped[bool] = mapped_column(Boolean)
    error: Mapped[str] = mapped_column(Text, nullable=True)
    state: Mapped[str] = mapped_column(String(255))
    raw_report_url: Mapped[str] = mapped_column(Text)
    raw_json: Mapped[Optional[List[str]]] = mapped_column(JSON)
    created_at = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
        server_default=text("NOW()")
    )
    
    def to_response(self):
        pass

"""
    PREDICTION
"""
    
class Prediction(Base):
    __tablename__ = 'predictions'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    identifier: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    
class PredictionReport(Base):
    __tablename__ = 'predictions_reports'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    prediction_id: Mapped[int] = mapped_column(Integer, ForeignKey("predictions.id"))
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("reports.id"))
    order: Mapped[int] = mapped_column(Integer, nullable=True)
    excluded: Mapped[bool] = mapped_column(Boolean)
    obsolate: Mapped[bool] = mapped_column(Boolean)
    value: Mapped[decimal.Decimal] = mapped_column(DECIMAL(precision=5, scale=1), nullable=True)
    
    def to_response(self):
        pass

"""
    USER WARNINGS
"""

class Game(Base):
    __tablename__ = 'games'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    identifier: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))

class UserWarning(Base):
    __tablename__ = 'user_warnings'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("reports.id"))
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"))
    level: Mapped[Enum] = mapped_column(Enum(LevelEnum), default=LevelEnum.DEFAULT)
    category: Mapped[Enum] = mapped_column(Enum(CategoryEnum), default=CategoryEnum.DEFAULT)
    message: Mapped[str] = mapped_column(Text)

class ReportLink(Base):
    __tablename__ = 'report_links'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("reports.id"))
    type: Mapped[Enum] = mapped_column(Enum(TypeEnum), nullable=True)
    url: Mapped[str] = mapped_column(String(255))

"""
    PROFILE MATCH
"""

class ProfileMatchCalculatorConfigs(Base):
    __tablename__ = 'profile_match_calculator_configs'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    identifier: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))

class ProfileMatchCalculatorFunction(Base):
    __tablename__ = 'profile_match_calculator_functions'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    identifier: Mapped[str] = mapped_column(String(255))

class ProfileMatchCalculator(Base):
    __tablename__ = 'profile_match_calculators'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    display_name: Mapped[str] = mapped_column(String(255))
    function_id: Mapped[int] = mapped_column(Integer, ForeignKey("profile_match_calculator_functions.id"))
    config_id: Mapped[int] = mapped_column(Integer, ForeignKey("profile_match_calculator_configs.id"))

class ProfileMatch(Base):
    __tablename__ = 'profile_matches'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("reports.id"))
    calculator_id: Mapped[int] = mapped_column(Integer, ForeignKey("profile_match_calculators.id"))
    error: Mapped[str] = mapped_column(Text, nullable=True)
    manual: Mapped[bool] = mapped_column(Boolean)
    value: Mapped[decimal.Decimal] = mapped_column(DECIMAL(precision=5, scale=2))
    model1_score: Mapped[decimal.Decimal] = mapped_column(DECIMAL(precision=10, scale=8))
    model1_score_perc: Mapped[decimal.Decimal] = mapped_column(DECIMAL(precision=5, scale=2))
    warnings: Mapped[str] = mapped_column(Text)
    gps_list: Mapped[Optional[List[str]]] = mapped_column(JSON)
    created_at = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
        server_default=text("NOW()")
    )