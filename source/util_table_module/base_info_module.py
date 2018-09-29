from sqlalchemy import Column, String, Integer, Float, DATETIME, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class S_Info(Base):
    __tablename__ = 's_info'

    id = Column(Integer, primary_key=True)
    ts_code = Column(String(12), nullable=True, default=None)
    code = Column(String(12), nullable=True, default=None)
    name = Column(String(100), nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)


class Security_Status(Base):
    __tablename__ = 'security_status'

    id = Column(Integer, primary_key=True)
    ts_code = Column(String(12), nullable=True, default=None)
    normal_status = Column(Boolean, nullable=True, default=None)
    tactics_1_status = Column(Boolean, nullable=True, default=None)
    tactics_2_status = Column(Boolean, nullable=True, default=None)
    tactics_3_status = Column(Boolean, nullable=True, default=None)
    tactics_4_status = Column(Boolean, nullable=True, default=None)
    tactics_5_status = Column(Boolean, nullable=True, default=None)
    tactics_6_status = Column(Boolean, nullable=True, default=None)
    tactics_7_status = Column(Boolean, nullable=True, default=None)
    tactics_8_status = Column(Boolean, nullable=True, default=None)
    tactics_9_status = Column(Boolean, nullable=True, default=None)
    tactics_10_status = Column(Boolean, nullable=True, default=None)
    tactics_11_status = Column(Boolean, nullable=True, default=None)
    tactics_12_status = Column(Boolean, nullable=True, default=None)
    tactics_13_status = Column(Boolean, nullable=True, default=None)
    tactics_14_status = Column(Boolean, nullable=True, default=None)
    tactics_15_status = Column(Boolean, nullable=True, default=None)
    tactics_16_status = Column(Boolean, nullable=True, default=None)
    tactics_17_status = Column(Boolean, nullable=True, default=None)
    tactics_18_status = Column(Boolean, nullable=True, default=None)
    tactics_19_status = Column(Boolean, nullable=True, default=None)
    tactics_20_status = Column(Boolean, nullable=True, default=None)


class Failed_Code(Base):
    __tablename__ = 'failed_code'

    id = Column(Integer, primary_key=True)
    code = Column(String(12), nullable=True, default=None)
    index = Column(String(12), nullable=True, default=None)
    error_message = Column(String(10000), nullable=True, default=None)
    date = Column(DATETIME, nullable=True, default=None)
    update_date = Column(DATETIME, nullable=True, default=None)


class Sec_Date_Info(Base):
    __tablename__ = 'sec_date_info'

    id = Column(Integer, primary_key=True)
    date = Column(Integer, nullable=True, default=None)
    is_workday_flag = Column(Integer, nullable=True, default=0)
