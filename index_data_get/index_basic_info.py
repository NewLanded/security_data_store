import datetime
import time

import pandas as pd
import tushare as ts

from conf import PRO_KEY
from util_base.date_util import convert_str_to_datetime
from util_base.db_util import get_connection, store_failed_message

ts.set_token(PRO_KEY)
pro = ts.pro_api()

"""
没能解决删除在插入新数据失败的时候删除旧数据的问题
"""
# def get_index_basic_data(market):
#     time.sleep(1)
#     index_basic_data = pro.index_basic(market=market)
#     index_basic_data = index_basic_data.where((pd.notnull(index_basic_data)), None)
#     time.sleep(1)
#     return index_basic_data
#
#
# def store_index_basic_data(session, one_index_basic_data):
#     new_data = Index_Basic_Info(ts_code=one_index_basic_data["ts_code"],
#                                 name=one_index_basic_data["name"],
#                                 market=one_index_basic_data["market"],
#                                 publisher=one_index_basic_data["publisher"],
#                                 category=one_index_basic_data["category"],
#                                 base_date=convert_str_to_datetime(one_index_basic_data["base_date"]) if one_index_basic_data["base_date"] and isinstance(
#                                     one_index_basic_data["base_date"], str) else one_index_basic_data["base_date"],
#                                 base_point=one_index_basic_data["base_point"],
#                                 list_date=convert_str_to_datetime(one_index_basic_data["list_date"]) if one_index_basic_data["list_date"] and isinstance(
#                                     one_index_basic_data["list_date"], str) else one_index_basic_data["list_date"],
#                                 update_date=datetime.datetime.now())
#     session.add(new_data)
#     session.commit()
#
#
# def start(market="SW"):
#     session = get_connection()
#     try:
#         session.query(Index_Basic_Info).delete()
#         session.commit()
#
#         index_basic_data = get_index_basic_data(market)
#         for index, one_index_basic_data in index_basic_data.iterrows():
#             store_index_basic_data(session, one_index_basic_data)
#     except Exception as e:
#         session.rollback()
#         store_failed_message(session, "", "000005", str(e), datetime.datetime.now())
#
#     session.close()


if __name__ == "__main__":
    pass
    # start()
    a = 1
    index_basic_data = pro.index_basic(market="SW")
    print(index_basic_data)
    pass
