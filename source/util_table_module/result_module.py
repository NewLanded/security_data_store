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


class Static_Invest(Base):
    __tablename__ = 'static_invest'

    id = Column(Integer, primary_key=True)
    ts_code = Column(String(12), nullable=True, default=None)
    name = Column(String(100), nullable=True, default=None)
    open_point = Column(Float)
    hold_cost = Column(Float)
    buy_percent = Column(Float)
    sell_percent = Column(Float)
    sent_flag = Column(TINYINT, nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)


class Tactics_Success_Rate(Base):
    __tablename__ = 'tactics_success_rate'

    id = Column(Integer, primary_key=True)
    tactics_code = Column(String(50), nullable=True, default=None)
    raise_sec_num = Column(Integer, nullable=True, default=None)
    all_sec_num = Column(Integer, nullable=True, default=None)
    raise_percent = Column(Float, nullable=True, default=None)
    forecast_date = Column(DATETIME, nullable=True, default=None)
    success_rate_3_day = Column(Float, nullable=True, default=None)
    success_rate_5_day = Column(Float, nullable=True, default=None)
    success_rate_7_day = Column(Float, nullable=True, default=None)
    gain_loss_3_day = Column(Float, nullable=True, default=None)
    gain_loss_5_day = Column(Float, nullable=True, default=None)
    gain_loss_7_day = Column(Float, nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)


class Tactics_Break_Ori_Point_Success_Rate(Base):
    __tablename__ = 'tactics_break_ori_point_success_rate'

    id = Column(Integer, primary_key=True)
    tactics_code = Column(String(50), nullable=True, default=None)
    forecast_date = Column(DATETIME, nullable=True, default=None)
    break_ori_point_sec_num_in_3_day = Column(Integer, nullable=True, default=None)
    break_ori_point_sec_num_in_5_day = Column(Integer, nullable=True, default=None)
    break_ori_point_sec_num_in_7_day = Column(Integer, nullable=True, default=None)
    all_sec_num = Column(Integer, nullable=True, default=None)
    break_in_3_day_rate_avg_7_day = Column(Float, nullable=True, default=None)
    break_in_5_day_rate_avg_7_day = Column(Float, nullable=True, default=None)
    break_in_7_day_rate_avg_7_day = Column(Float, nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)
