import datetime
import time

import pandas as pd
import tushare as ts

from source.conf import PRO_KEY
from source.util_base.date_util import convert_str_to_datetime
from source.util_base.db_util import get_connection, store_failed_message
from source.util_table_module.index_module import Index_Basic_Info

ts.set_token(PRO_KEY)
pro = ts.pro_api()

"""
未找到 从指标代码获取指数权重(index_weight接口)的有效的日期, 本接口暂时不使用
"""
def get_index_basic_data(market):
    time.sleep(1)
    index_basic_data = pro.index_basic(market=market)
    index_basic_data = index_basic_data.where((pd.notnull(index_basic_data)), None)
    time.sleep(1)
    return index_basic_data


def store_index_basic_data(session, one_index_basic_data):
    new_data = Index_Basic_Info(ts_code=one_index_basic_data["ts_code"],
                                name=one_index_basic_data["name"],
                                market=one_index_basic_data["market"],
                                publisher=one_index_basic_data["publisher"],
                                category=one_index_basic_data["category"],
                                base_date=convert_str_to_datetime(one_index_basic_data["base_date"]) if one_index_basic_data["base_date"] and isinstance(
                                    one_index_basic_data["base_date"], str) else one_index_basic_data["base_date"],
                                base_point=one_index_basic_data["base_point"],
                                list_date=convert_str_to_datetime(one_index_basic_data["list_date"]) if one_index_basic_data["list_date"] and isinstance(
                                    one_index_basic_data["list_date"], str) else one_index_basic_data["list_date"],
                                update_date=datetime.datetime.now())
    session.add(new_data)
    session.commit()


def start(market="CSI"):
    session = get_connection()
    try:
        session.query(Index_Basic_Info).delete()
        session.commit()

        index_basic_data = get_index_basic_data(market)
        for index, one_index_basic_data in index_basic_data.iterrows():
            store_index_basic_data(session, one_index_basic_data)
    except Exception as e:
        session.rollback()
        store_failed_message(session, "", "000005", str(e), datetime.datetime.now())

    session.close()


if __name__ == "__main__":
    pass
    start()
    # a = 1
    # index_basic_data = pro.index_basic(market="SW")
    pass
