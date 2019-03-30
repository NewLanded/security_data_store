import datetime
import time

import pandas as pd
import tushare as ts

from conf import PRO_KEY
from util_base.date_util import convert_datetime_to_str, convert_str_to_datetime
from util_base.db_util import engine
from util_base.db_util import store_failed_message
from util_data.date import Date

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_all_security_daily_basic(data_date_str):
    time.sleep(2)
    all_security_daily_basic = pro.daily_basic(trade_date=data_date_str)
    all_security_daily_basic = all_security_daily_basic.where((pd.notnull(all_security_daily_basic)), None)
    time.sleep(2)
    return all_security_daily_basic


def store_security_daily_basic(security_daily_basic_data):
    security_daily_basic_data["update_date"] = datetime.datetime.now()
    security_daily_basic_data["trade_date"] = security_daily_basic_data["trade_date"].apply(convert_str_to_datetime)
    security_daily_basic_data["turnover_rate"] = security_daily_basic_data["turnover_rate"].apply(lambda x: x / 100)
    security_daily_basic_data["turnover_rate_f"] = security_daily_basic_data["turnover_rate_f"].apply(lambda x: x / 100)

    security_daily_basic_data.to_sql("security_daily_basic", engine, index=False, if_exists="append")


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    if Date().is_workday(date_now):
        try:
            all_security_daily_basic = get_all_security_daily_basic(convert_datetime_to_str(date_now))
            store_security_daily_basic(all_security_daily_basic)
        except Exception as e:
            store_failed_message("", "000005", str(e), date_now)


if __name__ == "__main__":
    # start(datetime.datetime(2019, 3, 21))
    # all_security_daily_basic = pro.daily_basic(trade_date="20181008")
    pass