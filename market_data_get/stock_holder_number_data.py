import datetime
import time

import tushare as ts

from conf import PRO_KEY
from util_base.date_util import convert_datetime_to_str, convert_str_to_datetime
from util_base.db_util import engine
from util_base.db_util import store_failed_message
from util_data.market import Market
from util_data.stock import Stock

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_ts_code_list():
    all_stocks_info = Stock().get_all_stocks_info()
    ts_code_list = list(all_stocks_info)
    return ts_code_list


def get_holder_number(ts_code, start_date, end_date):
    time.sleep(1)
    holder_number_data = pro.stk_holdernumber(ts_code=ts_code, start_date=convert_datetime_to_str(start_date), end_date=convert_datetime_to_str(end_date))
    return holder_number_data


def get_db_holder_number(ts_code, start_date, end_date):
    holder_number_data = Market().get_holder_number_data(ts_code, start_date, end_date)
    return holder_number_data


def update_holder_number(holder_number, db_holder_number, ts_code, start_date, end_date):
    if len(holder_number) != len(db_holder_number):
        holder_number["update_date"] = datetime.datetime.now()
        holder_number["ann_date"] = holder_number["ann_date"].apply(convert_str_to_datetime)
        holder_number["end_date"] = holder_number["end_date"].apply(convert_str_to_datetime)

        Market().delete_holder_number_data(ts_code, start_date, end_date)
        holder_number.to_sql("holder_number_data", engine, index=False, if_exists="append")


def start(start_date=None, end_date=None):  # 公告开始日期, 公告结束日期
    """
    :param start_date:  公告开始日期
    :param end_date:  公告结束日期
    Nonte:
        公告日期写当天的话, 有可能数据查不到, 所以写一段时间, 有新数据就全量替换
    """
    if end_date is None:
        end_date = datetime.datetime.now()
        end_date = datetime.datetime(end_date.year, end_date.month, end_date.day)

    if start_date is None:
        start_date = end_date - datetime.timedelta(days=360)

    ts_code_list = get_ts_code_list()

    for ts_code in ts_code_list:
        try:
            holder_number = get_holder_number(ts_code, start_date, end_date)
            db_holder_number = get_db_holder_number(ts_code, start_date, end_date)
            update_holder_number(holder_number, db_holder_number, ts_code, start_date, end_date)
        except Exception as e:
            store_failed_message("", "stock_holder_number_data", str(e), end_date)


if __name__ == "__main__":
    pass
    start(end_date=datetime.datetime(2019, 11, 6))
    # all_security_point_data = pro.daily(trade_date="20181008")
    pass
