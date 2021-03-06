import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from conf import DB_CONNECT

engine = create_engine(DB_CONNECT, echo=False, pool_recycle=360)
DBSession = sessionmaker(bind=engine)


def get_connection():
    session = DBSession()
    return session


def store_data(sql, args=None):
    session = get_connection()
    if args:
        session.execute(text(sql), args)
    else:
        session.execute(text(sql))
    session.commit()
    session.close()


def get_multi_data(sql, args=None):
    session = get_connection()
    try:
        if args:
            result_proxy = session.execute(text(sql), args)
        else:
            result_proxy = session.execute(text(sql))
        result = result_proxy.fetchall()
    finally:
        session.close()
    return result


def update_data(sql, args=None):
    session = get_connection()
    try:
        if args is None:
            session.execute(sql)
        else:
            session.execute(sql, args)
        session.commit()
    except Exception as e:
        raise e
    finally:
        session.close()


def store_failed_message(code, index, error_message, date):
    sql = """
    insert into failed_code(code, index, error_message, date, update_date) values(:code, :index, :error_message, :date, :update_date)
    """
    args = {"code": code, "index": index, "error_message": error_message, "date": date, "update_date": datetime.datetime.now()}
    store_data(sql, args)

# import mysql.connector.pooling
#
# from config import db_config
#
#
# class MySQLPool(object):
#     """
#     create a pool when connect mysql, which will decrease the time spent in
#     request connection, create connection and close connection.
#     """
#
#     def __init__(self, host="172.0.0.1", port="3306", user="root", password="123456", database="test",
#                  pool_name="my_pool", pool_size=3):
#         res = {}
#         self._host = host
#         self._port = port
#         self._user = user
#         self._password = password
#         self._database = database
#
#         res["host"] = self._host
#         res["port"] = self._port
#         res["user"] = self._user
#         res["password"] = self._password
#         res["database"] = self._database
#         self.db_config = res
#         self.pool = self.create_pool(pool_name=pool_name, pool_size=pool_size)
#
#     def create_pool(self, pool_name="mypool", pool_size=3):
#         """
#         Create a connection pool, after created, the request of connecting
#         MySQL could get a connection from this pool instead of request to
#         create a connection.
#         :param pool_name: the name of pool, default is "mypool"
#         :param pool_size: the size of pool, default is 3
#         :return: connection pool
#         """
#         pool = mysql.connector.pooling.MySQLConnectionPool(pool_name=pool_name, pool_size=pool_size,
#                                                            pool_reset_session=True, **self.db_config)
#         return pool
#
#     def close(self, conn, cursor):
#         """
#         A method used to close connection of mysql.
#         :param conn:
#         :param cursor:
#         :return:
#         """
#         cursor.close()
#         conn.close()
#
#     def execute(self, sql, args=None, commit=False):
#         """
#         Execute a sql, it could be with args and with out args. The usage is
#         similar with execute() function in util_table_module pymysql.
#         :param sql: sql clause
#         :param args: args need by sql clause
#         :param commit: whether to commit
#         :return: if commit, return None, else, return result
#         """
#         # get connection form connection pool instead of create one.
#         conn = self.pool.get_connection()
#         cursor = conn.cursor()
#         if args:
#             cursor.execute(sql, args)
#         else:
#             cursor.execute(sql)
#         if commit is True:
#             conn.commit()
#             self.close(conn, cursor)
#             return None
#         else:
#             res = cursor.fetchall()
#             self.close(conn, cursor)
#             return res
#
#     def executemany(self, sql, args, commit=False):
#         """
#         Execute with many args. Similar with executemany() function in pymysql.
#         args should be a sequence.
#         :param sql: sql clause
#         :param args: args
#         :param commit: commit or not.
#         :return: if commit, return None, else, return result
#         """
#         # get connection form connection pool instead of create one.
#         conn = self.pool.get_connection()
#         cursor = conn.cursor()
#         cursor.executemany(sql, args)
#         if commit is True:
#             conn.commit()
#             self.close(conn, cursor)
#             return None
#         else:
#             res = cursor.fetchall()
#             self.close(conn, cursor)
#             return res
#
#
# if __name__ == "__main__":
#     mysql_pool = MySQLPool(**db_config)
#     sql = "select * from store WHERE create_time < '2017-06-02'"
#     mysql_pool.execute(sql)
