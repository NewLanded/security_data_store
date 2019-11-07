import datetime
import time

import tushare as ts

from conf import PRO_KEY
from util_base.date_util import convert_datetime_to_str, convert_str_to_datetime, get_date_range
from util_base.db_util import engine
from util_base.db_util import store_failed_message
from util_data.date import Date

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_all_index_point_data(data_date_str):
    time.sleep(2)
    all_index_point_data = pro.index_daily(ts_code='399300.SZ', trade_date=data_date_str)
    time.sleep(2)
    return all_index_point_data


def store_index_point_data(index_point_data):
    index_point_data["update_date"] = datetime.datetime.now()
    index_point_data["trade_date"] = index_point_data["trade_date"].apply(convert_str_to_datetime)
    index_point_data["pct_chg"] = index_point_data["pct_chg"].apply(lambda x: x / 100)

    index_point_data.to_sql("index_point_data", engine, index=False, if_exists="append")


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    if Date().is_workday(date_now):
        try:
            all_index_point_data = get_all_index_point_data(convert_datetime_to_str(date_now))
            store_index_point_data(all_index_point_data)
        except Exception as e:
            store_failed_message("index_point_data", "000005", str(e), date_now)


if __name__ == "__main__":
    pass
    # for date in get_date_range(datetime.datetime(2015, 12, 28), datetime.datetime(2019, 3, 21)):
    #     start(date)
    start(datetime.datetime(2019, 3, 21))
    # all_index_point_data = pro.df = pro.index_daily(ts_code='399300.SZ', trade_date="20190321")
    a = 1
    pass
