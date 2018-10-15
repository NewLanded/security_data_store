from sqlalchemy import Column, String, Integer, Float, DATETIME, Boolean

from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BS_Data(Base):
    __tablename__ = 'bs_data'

    id = Column(Integer, primary_key=True)
    code = Column(String(6), nullable=True, default=None)
    b_point = Column(Float)
    s_point = Column(Float)
    quantity = Column(Integer, nullable=True, default=None)
    tactics_code = Column(String(50), nullable=True, default=None)
    sent_flag = Column(TINYINT, nullable=True, default=None)
    raise_flag = Column(Boolean, nullable=True, default=None)
    raise_pct_change = Column(Float, nullable=True, default=None)
    forecast_date = Column(DATETIME, nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)


class Tactics_Success_Rate(Base):
    __tablename__ = 'tactics_success_rate'

    id = Column(Integer, primary_key=True)
    tactics_code = Column(String(50), nullable=True, default=None)
    success_rate_3_day = Column(Float, nullable=True, default=None)
    success_rate_5_day = Column(Float, nullable=True, default=None)
    success_rate_7_day = Column(Float, nullable=True, default=None)
    success_rate_1_month = Column(Float, nullable=True, default=None)
    success_rate_3_month = Column(Float, nullable=True, default=None)
    success_rate_6_month = Column(Float, nullable=True, default=None)
    success_rate_12_month = Column(Float, nullable=True, default=None)
    gain_loss_3_day = Column(Float, nullable=True, default=None)
    gain_loss_5_day = Column(Float, nullable=True, default=None)
    gain_loss_7_day = Column(Float, nullable=True, default=None)
    gain_loss_1_month = Column(Float, nullable=True, default=None)
    gain_loss_3_month = Column(Float, nullable=True, default=None)
    gain_loss_6_month = Column(Float, nullable=True, default=None)
    gain_loss_12_month = Column(Float, nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)
