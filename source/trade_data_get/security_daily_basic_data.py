import datetime
import time

import pandas as pd
import tushare as ts

from source.conf import PRO_KEY
from source.util_base.date_util import convert_datetime_to_str
from source.util_base.db_util import get_connection, store_failed_message
from source.util_data.date import Date
from source.util_data.stock import Stock
from source.util_table_module.data_module import Security_Daily_Basic

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_all_security_daily_basic(data_date_str):
    time.sleep(1)
    all_security_daily_basic = pro.daily_basic(trade_date=data_date_str)
    all_security_daily_basic = all_security_daily_basic.where((pd.notnull(all_security_daily_basic)), None)
    time.sleep(1)
    return all_security_daily_basic


def store_security_daily_basic(session, security_daily_basic_data):
    new_data = Security_Daily_Basic(ts_code=security_daily_basic_data["ts_code"], trade_date=security_daily_basic_data["trade_date"],
                                    close=security_daily_basic_data["close"],
                                    turnover_rate=security_daily_basic_data["turnover_rate"], volume_ratio=security_daily_basic_data["volume_ratio"],
                                    pe=security_daily_basic_data["pe"], pe_ttm=security_daily_basic_data["pe_ttm"], pb=security_daily_basic_data["pb"],
                                    ps=security_daily_basic_data["ps"], ps_ttm=security_daily_basic_data["ps_ttm"],
                                    total_share=security_daily_basic_data["total_share"],
                                    float_share=security_daily_basic_data["float_share"], free_share=security_daily_basic_data["free_share"],
                                    total_mv=security_daily_basic_data["total_mv"], circ_mv=security_daily_basic_data["circ_mv"],
                                    update_date=datetime.datetime.now())
    session.add(new_data)
    session.commit()


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    session = get_connection()

    if Date().is_workday(date_now):
        try:
            all_security_daily_basic = get_all_security_daily_basic(convert_datetime_to_str(date_now))
            for index, security_daily_basic_data in all_security_daily_basic.iterrows():
                if Stock().is_valid_security_normal(security_daily_basic_data["ts_code"]):
                    store_security_daily_basic(session, security_daily_basic_data)
        except Exception as e:
            session.rollback()
            store_failed_message(session, "", "000003", str(e), date_now)

    session.close()


if __name__ == "__main__":
    # start(datetime.datetime(2018, 5, 31))
    all_security_daily_basic = pro.daily_basic(trade_date="20181008")
    pass
