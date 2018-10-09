from sqlalchemy import Column, String, Integer, Float, DATETIME, Boolean
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
    sent_flag = Column(Boolean)
    update_date = Column(DATETIME, nullable=True, default=None)
