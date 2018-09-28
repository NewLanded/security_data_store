from sqlalchemy import Column, String, Integer, Float, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class S_Info(Base):
    __tablename__ = 's_info'

    id = Column(Integer, primary_key=True)
    code = Column(String(6), nullable=True, default=None)
    name = Column(String(100), nullable=True, default=None)
    hs300_weight = Column(Float, nullable=True, default=None)
    data_date = Column(DATETIME, nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)


class Failed_Code(Base):
    __tablename__ = 'failed_code'

    id = Column(Integer, primary_key=True)
    code = Column(String(6), nullable=True, default=None)
    index = Column(String(6), nullable=True, default=None)
    error_message = Column(String(10000), nullable=True, default=None)
    date = Column(DATETIME, nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)


class Sec_Date_Info(Base):
    __tablename__ = 'sec_date_info'

    id = Column(Integer, primary_key=True)
    date = Column(Integer, nullable=True, default=None)
    is_workday_flag = Column(Integer, nullable=True, default=0)

