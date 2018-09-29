import datetime
import time

import tushare as ts

from source.conf import PRO_KEY
from source.util_base.date_util import convert_datetime_to_str, get_date_range
from source.util_base.db_util import get_connection, store_failed_message
from source.util_data.date import Date
from source.util_data.stock import Stock
from source.util_table_module.base_info_module import S_Info
from source.util_table_module.data_module import Security_Point_Data

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_ts_codes(session):
    ts_codes = session.query(S_Info.ts_code).all()
    ts_codes = [i[0] for i in ts_codes]
    return ts_codes


def get_security_point_data(ts_code, start_date_str, end_date_str):
    time.sleep(1)
    security_point_data = pro.daily(ts_code=ts_code, start_date=start_date_str, end_date=end_date_str)
    return security_point_data


def store_security_point_data(session, security_point_data):
    for index, data in security_point_data.iterrows():
        new_data = Security_Point_Data(ts_code=data["ts_code"], trade_date=data["trade_date"], open=data["open"],
                                       high=data["high"], low=data["low"],
                                       close=data["close"], pre_close=data["pre_close"], change=data["change"],
                                       pct_change=data["pct_change"], vol=data["vol"], amount=data["amount"],
                                       update_date=datetime.datetime.now())
        session.add(new_data)
        session.commit()


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    session = get_connection()

    if Date().is_workday(date_now):
        ts_codes = get_ts_codes(session)
        start_date, end_date = date_now, date_now
        for ts_code in ts_codes:
            if Stock().is_valid_security_normal(ts_code):
                try:
                    security_point_data = get_security_point_data(ts_code, convert_datetime_to_str(start_date),
                                                                  convert_datetime_to_str(end_date))
                    store_security_point_data(session, security_point_data)
                except Exception as e:
                    store_failed_message(session, ts_code, "000002", str(e), None)
    session.close()


if __name__ == "__main__":
    start()
    # for date in get_date_range(datetime.datetime(2018, 6, 1), datetime.datetime(2018, 6, 3)):
    #     start(date)
