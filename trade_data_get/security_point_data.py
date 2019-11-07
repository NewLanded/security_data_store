import datetime
import time

import tushare as ts

from conf import PRO_KEY
from util_base.date_util import convert_datetime_to_str, convert_str_to_datetime
from util_base.db_util import engine
from util_base.db_util import store_failed_message
from util_data.date import Date

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_all_security_point_data(data_date_str):
    time.sleep(2)
    all_security_point_data = pro.daily(trade_date=data_date_str)
    time.sleep(2)
    return all_security_point_data


def store_security_point_data(security_point_data):
    security_point_data["update_date"] = datetime.datetime.now()
    security_point_data["trade_date"] = security_point_data["trade_date"].apply(convert_str_to_datetime)
    security_point_data["pct_chg"] = security_point_data["pct_chg"].apply(lambda x: x / 100)

    security_point_data.to_sql("security_point_data", engine, index=False, if_exists="append")


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    if Date().is_workday(date_now):
        try:
            all_security_point_data = get_all_security_point_data(convert_datetime_to_str(date_now))
            store_security_point_data(all_security_point_data)
        except Exception as e:
            store_failed_message("security_point_data", "000005", str(e), date_now)


if __name__ == "__main__":
    pass
    start(datetime.datetime(2019, 3, 21))
    # all_security_point_data = pro.daily(trade_date="20181008")
    pass
