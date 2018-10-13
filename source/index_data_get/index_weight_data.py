import datetime
import time

import tushare as ts

from source.conf import PRO_KEY
from source.util_base.date_util import convert_str_to_datetime, get_date_range, convert_datetime_to_str
from source.util_base.db_util import get_connection, store_failed_message
from source.util_data.date import Date
from source.util_data.index import Index
from source.util_table_module.index_module import Index_Weight_Data

ts.set_token(PRO_KEY)
pro = ts.pro_api()

"""
现在这个接口取得是沪深300的指数权重, 还不清楚怎么弄其他指数, 而且hs300的指数也取不到最近几天的
"""
def get_index_weight_data(ts_index_code, date_now):
    time.sleep(1)
    index_weight_data = pro.index_weight(index_code=ts_index_code, trade_date=date_now)
    time.sleep(1)
    return index_weight_data


def store_index_weight_data(session, one_index_weight_data):
    new_data = Index_Weight_Data(index_code=one_index_weight_data["index_code"],
                                 con_code=one_index_weight_data["con_code"],
                                 trade_date=convert_str_to_datetime(one_index_weight_data["trade_date"]) if one_index_weight_data["trade_date"] and isinstance(
                                     one_index_weight_data["trade_date"], str) else one_index_weight_data["trade_date"],
                                 weight=one_index_weight_data["weight"],
                                 update_date=datetime.datetime.now())
    session.add(new_data)
    session.commit()


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    session = get_connection()
    if Date().is_workday(date_now):
        try:
            session.query(Index_Weight_Data).delete()
            session.commit()

            index_weight_data = get_index_weight_data('399300.SZ', convert_datetime_to_str(date_now))
            for index, one_index_weight_data in index_weight_data.iterrows():
                store_index_weight_data(session, one_index_weight_data)

                # index_basic_info = Index().get_index_basic_info("SW")
                # for ts_index_code, ts_code_data in index_basic_info.items():
                #     index_basic_data = get_index_weight_data(ts_index_code)
                #     for index, one_index_basic_data in index_basic_data.iterrows():
                #         store_index_basic_data(session, one_index_basic_data)
        except Exception as e:
            session.rollback()
            store_failed_message(session, "", "000005", str(e), datetime.datetime.now())

    session.close()


if __name__ == "__main__":
    pass
    start(datetime.datetime(2018, 9, 28))
    pass
