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
    pct_change = Column(Float, nullable=True, default=None)
    vol = Column(Float, nullable=True, default=None)
    amount = Column(Float, nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)
