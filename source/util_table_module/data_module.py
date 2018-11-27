from sqlalchemy import Column, String, Integer, Float, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Security_Point_Data(Base):
    __tablename__ = 'security_point_data'

    id = Column(Integer, primary_key=True)
    ts_code = Column(String(12), nullable=True, default=None)
    trade_date = Column(DATETIME, nullable=True, default=None)
    open = Column(Float, nullable=True, default=None)
    high = Column(Float, nullable=True, default=None)
    low = Column(Float, nullable=True, default=None)
    close = Column(Float, nullable=True, default=None)
    pre_close = Column(Float, nullable=True, default=None)
    change = Column(Float, nullable=True, default=None)
    pct_chg = Column(Float, nullable=True, default=None)
    vol = Column(Float, nullable=True, default=None)
    amount = Column(Float, nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)


class Security_Daily_Basic(Base):
    __tablename__ = 'security_daily_basic'

    id = Column(Integer, primary_key=True)
    ts_code = Column(String(12), nullable=True, default=None)
    trade_date = Column(DATETIME, nullable=True, default=None)
    close = Column(Float, nullable=True, default=None)
    turnover_rate = Column(Float, nullable=True, default=None)
    volume_ratio = Column(Float, nullable=True, default=None)
    pe = Column(Float, nullable=True, default=None)
    pe_ttm = Column(Float, nullable=True, default=None)
    pb = Column(Float, nullable=True, default=None)
    ps = Column(Float, nullable=True, default=None)
    ps_ttm = Column(Float, nullable=True, default=None)
    total_share = Column(Float, nullable=True, default=None)
    float_share = Column(Float, nullable=True, default=None)
    free_share = Column(Float, nullable=True, default=None)
    total_mv = Column(Float, nullable=True, default=None)
    circ_mv = Column(Float, nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)
