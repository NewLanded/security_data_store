import datetime
import time
import re
import tushare as ts
import pandas as pd

from conf import PRO_KEY, FUTURE_EXCHANGE_CODE_LIST
from util_base.date_util import convert_datetime_to_str, convert_str_to_datetime, get_date_range
from util_base.db_util import engine, update_data, get_multi_data
from util_base.db_util import store_failed_message
from util_data.date import Date

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_future_holding_data(data_date_str, exchange):
    future_holding_data = pro.fut_holding(trade_date=data_date_str, exchange=exchange)
    time.sleep(2)

    # 大商所从2021-03-31之后就不返回主力合约的持仓了, 这里手工加上
    data_date = convert_str_to_datetime(data_date_str)
    if exchange == "DCE" and data_date > datetime.datetime(2021, 3, 31):
        sql = """
        select ts_code, mapping_ts_code from future_main_code_data where trade_date=:data_date
        """
        args = {"data_date": data_date}
        result = dict(get_multi_data(sql, args))

        symbol_list = list(set(list(future_holding_data['symbol'])))
        main_symbol_list = []
        for symbol in symbol_list:
            main_code_re = re.match(r'\D+', symbol, re.I)
            if main_code_re:
                main_symbol_list.append(main_code_re.group())
        main_symbol_list = list(set(main_symbol_list))
        main_symbol_list.sort()

        for symbol in main_symbol_list:
            mapping_code = result.get(symbol + ".DCE")
            if mapping_code:
                mapping_code = mapping_code.split(".")[0]
                main_code_result = future_holding_data[future_holding_data['symbol'] == mapping_code].copy()
                main_code_result['symbol'] = symbol
                future_holding_data = pd.concat([future_holding_data, main_code_result])

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
    for date_now in get_date_range(datetime.datetime(2015, 1, 1), datetime.datetime(2021, 6, 18)):
        print(date_now)
        start(date_now)
    # start(datetime.datetime(2020, 5, 19))
    # all_future_daily_point_data = pro.daily(trade_date="20181008")
    pass
