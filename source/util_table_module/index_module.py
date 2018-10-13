from sqlalchemy import Column, String, Integer, Float, DATETIME

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Index_Basic_Info(Base):
    __tablename__ = 'index_basic_info'

    id = Column(Integer, primary_key=True)
    ts_code = Column(String(12), nullable=True, default=None)
    name = Column(String(100), nullable=True, default=None)
    market = Column(String(20), nullable=True, default=None)
    publisher = Column(String(50), nullable=True, default=None)
    category = Column(String(50), nullable=True, default=None)
    base_date = Column(DATETIME, nullable=True, default=None)
    base_point = Column(Float, nullable=True, default=None)
    list_date = Column(DATETIME, nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)


class Index_Weight_Data(Base):
    __tablename__ = 'index_weight_data'

    id = Column(Integer, primary_key=True)
    index_code = Column(String(12), nullable=True, default=None)
    con_code = Column(String(12), nullable=True, default=None)
    trade_date = Column(DATETIME, nullable=True, default=None)
    weight = Column(Float, nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)
