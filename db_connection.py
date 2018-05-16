from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conf import DB_CONNECT


def get_connection():
    engine = create_engine(DB_CONNECT, echo=False)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session
