from sqlalchemy import Column, String, Integer, Float, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Hs300_Rehabilitation_Data(Base):
    __tablename__ = 'hs300_rehabilitation_data'

    id = Column(Integer, primary_key=True)
    code = Column(String(6), nullable=True, default=None)
    date = Column(DATETIME, nullable=True, default=None)
    open = Column(Float, nullable=True, default=None)
    high = Column(Float, nullable=True, default=None)
    close = Column(Float, nullable=True, default=None)
    low = Column(Float, nullable=True, default=None)
    volume = Column(Float, nullable=True, default=None)
    amount = Column(Float, nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)
