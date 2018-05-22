import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from source.conf import DB_CONNECT
from source.moudle.base_info_moudle import Failed_Code


def store_failed_message(session, code, index, error_message, date):
    data = Failed_Code(code=code, index=index, error_message=error_message, date=date,
                       update_date=datetime.datetime.now())
    session.add(data)
    session.commit()


def get_connection():
    engine = create_engine(DB_CONNECT, echo=False)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session
