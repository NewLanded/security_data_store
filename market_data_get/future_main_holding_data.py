import datetime
import time

import tushare as ts

from conf import PRO_KEY, FUTURE_EXCHANGE_CODE_LIST
from util_base.date_util import convert_datetime_to_str, convert_str_to_datetime, get_date_range
from util_base.db_util import engine, update_data
from util_base.db_util import store_failed_message
from util_data.date import Date

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_future_holding_data(data_date_str, exchange):
    future_holding_data = pro.fut_holding(trade_date=data_date_str, exchange=exchange)
    time.sleep(2)
    return future_holding_data


def store_future_holding_data(future_holding_data):
    future_holding_data["update_date"] = datetime.datetime.now()
    future_holding_data["trade_date"] = future_holding_data["trade_date"].apply(convert_str_to_datetime)

    future_holding_data.to_sql("future_holding_data", engine, index=False, if_exists="append")


def delete_future_holding_data(data_date):
    sql = """
    delete from future_holding_data where trade_date=:data_date
    """
    args = {"data_date": data_date}
    update_data(sql, args)


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    if Date().is_workday(date_now):
        delete_future_holding_data(date_now)
        for exchange in FUTURE_EXCHANGE_CODE_LIST:
            try:
                future_holding_data = get_future_holding_data(convert_datetime_to_str(date_now), exchange)
                store_future_holding_data(future_holding_data)
            except Exception as e:
                store_failed_message("", "future_main_holding_data", str(e), date_now)


if __name__ == "__main__":
    # for date_now in get_date_range(datetime.datetime(2019, 10, 1), datetime.datetime(2019, 11, 19)):
    #     print(date_now)
    #     start(date_now)
    start(datetime.datetime(2021, 4, 2))
