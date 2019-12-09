import datetime
import time

import tushare as ts

from conf import PRO_KEY, FUTURE_EXCHANGE_CODE_LIST
from util_base.date_util import convert_str_to_datetime
from util_base.db_util import engine
from util_base.db_util import store_data
from util_base.db_util import store_failed_message

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_future_basic_info_data(exchange):
    future_basic_info_data = pro.fut_basic(exchange=exchange)
    time.sleep(2)
    return future_basic_info_data


def delete_old_data():
    sql = """
    truncate table future_basic_info_data
    """
    store_data(sql)


def store_future_basic_info_data(future_basic_info_data, exchange):
    future_basic_info_data["update_date"] = datetime.datetime.now()
    future_basic_info_data["list_date"] = future_basic_info_data["list_date"].apply(convert_str_to_datetime)
    future_basic_info_data["delist_date"] = future_basic_info_data["delist_date"].apply(convert_str_to_datetime)
    future_basic_info_data["last_ddate"] = future_basic_info_data["last_ddate"].apply(convert_str_to_datetime)

    if exchange == 'CZCE':  # 郑商所symbol特殊, 做特殊处理
        future_basic_info_data['symbol'] = future_basic_info_data['ts_code'].apply(lambda x: x.split('.')[0])

    future_basic_info_data.to_sql("future_basic_info_data", engine, index=False, if_exists="append")


def start():
    date_now = datetime.datetime.now()
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    delete_old_data()
    for exchange in FUTURE_EXCHANGE_CODE_LIST:
        try:
            future_basic_info_data = get_future_basic_info_data(exchange)
            store_future_basic_info_data(future_basic_info_data, exchange)
        except Exception as e:
            store_failed_message("", "future_basic_info_data", str(e), date_now)


if __name__ == "__main__":
    start()
