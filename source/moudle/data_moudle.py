from sqlalchemy import Column, String, Integer, Float, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Hs300_Rehabilitation_Data(Base):
    __tablename__ = 'hs300_rehabilitation_data'

    id = Column(Integer, primary_key=True)
    code = Column(String(6), nullable=False)
    date = Column(DATETIME, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    # amount = Column(Float, nullable=False)
    update_date = Column(DATETIME, nullable=True)
