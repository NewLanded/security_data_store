import datetime

import tushare as ts

from source.conf import PRO_KEY
from source.util_base.db_util import get_connection, store_failed_message
from source.util_table_module.base_info_module import S_Info

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_stock_info():
    stock_info = pro.stock_basic(list_status='L', fields='ts_code, symbol, name')
    return stock_info


def store_stock_info(session, stock_info):
    for index, security_info in stock_info.iterrows():
        new_data = S_Info(ts_code=security_info["ts_code"], code=security_info["symbol"], name=security_info["name"],
                          update_date=datetime.datetime.now())
        session.add(new_data)
        session.commit()


def start():
    session = get_connection()

    try:
        stock_info = get_stock_info()
        store_stock_info(session, stock_info)
    except Exception as e:
        session.rollback()
        store_failed_message(session, None, "000001", str(e), datetime.date.today())
    session.close()


if __name__ == "__main__":
    start()
