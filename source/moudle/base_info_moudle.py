from sqlalchemy import Column, String, Integer, Float, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class S_Info(Base):
    __tablename__ = 's_info'

    id = Column(Integer, primary_key=True)
    code = Column(String(6), nullable=False)
    name = Column(String(100), nullable=False)
    hs300_weight = Column(Float, nullable=False)
    data_date = Column(DATETIME, nullable=False)
    update_date = Column(DATETIME, nullable=True)


class Failed_Code(Base):
    __tablename__ = 'failed_code'

    id = Column(Integer, primary_key=True)
    code = Column(String(6), nullable=False)
    index = Column(String(6), nullable=False)
    error_message = Column(String(10000), nullable=False)
    date = Column(DATETIME, nullable=False)
    update_date = Column(DATETIME, nullable=True)
