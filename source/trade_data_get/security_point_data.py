import datetime
import time

import tushare as ts

from source.conf import PRO_KEY
from source.util_base.date_util import convert_datetime_to_str
from source.util_base.db_util import get_connection, store_failed_message
from source.util_data.date import Date
from source.util_data.stock import Stock
from source.util_table_module.data_module import Security_Point_Data

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_all_security_point_data(data_date_str):
    time.sleep(1)
    all_security_point_data = pro.daily(trade_date=data_date_str)
    time.sleep(1)
    return all_security_point_data


def store_security_point_data(session, security_point_data):
    new_data = Security_Point_Data(ts_code=security_point_data["ts_code"], trade_date=security_point_data["trade_date"], open=security_point_data["open"],
                                   high=security_point_data["high"], low=security_point_data["low"],
                                   close=security_point_data["close"], pre_close=security_point_data["pre_close"], change=security_point_data["change"],
                                   pct_change=security_point_data["pct_change"], vol=security_point_data["vol"], amount=security_point_data["amount"],
                                   update_date=datetime.datetime.now())
    session.add(new_data)
    session.commit()


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    session = get_connection()

    if Date().is_workday(date_now):
        try:
            all_security_point_data = get_all_security_point_data(convert_datetime_to_str(date_now))
            for index, security_point_data in all_security_point_data.iterrows():
                if Stock().is_valid_security_normal(security_point_data["ts_code"]):
                    store_security_point_data(session, security_point_data)
        except Exception as e:
            store_failed_message(session, "", "000002", str(e), None)

    session.close()


if __name__ == "__main__":
    pass
    # start(datetime.datetime(2018, 5, 31))
