import datetime
import time

import tushare as ts

from conf import PRO_KEY
from util_base.date_util import convert_str_to_datetime, convert_datetime_to_str, get_date_range
from util_base.db_util import engine
from util_base.db_util import store_failed_message

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_future_main_code_data(date_now):
    future_main_code_data = pro.fut_mapping(trade_date=date_now)
    time.sleep(2)
    return future_main_code_data


def store_future_main_code_data(future_main_code_data):
    future_main_code_data["update_date"] = datetime.datetime.now()
    future_main_code_data["trade_date"] = future_main_code_data["trade_date"].apply(convert_str_to_datetime)

    future_main_code_data.to_sql("future_main_code_data", engine, index=False, if_exists="append")


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    try:
        future_main_code_data = get_future_main_code_data(convert_datetime_to_str(date_now))
        store_future_main_code_data(future_main_code_data)
    except Exception as e:
        store_failed_message("", "000006", str(e), date_now)


if __name__ == "__main__":
    for date_now in get_date_range(datetime.datetime(2019, 1, 1), datetime.datetime(2019, 11, 24)):
        print(date_now)
        start(date_now)
