import time

import pandas as pd
import tushare as ts

from conf import PRO_KEY
from util_base.date_util import convert_str_to_datetime
from util_base.db_util import store_data, engine

ts.set_token(PRO_KEY)
pro = ts.pro_api()

#
# def delete_old_data():
#     sql = """
#     truncate table index_basic_info
#     """
#     store_data(sql)
#
#
# def get_index_basic_info(market):
#     time.sleep(1)
#     index_basic_info = pro.index_basic(market=market)
#     index_basic_info = index_basic_info.where((pd.notnull(index_basic_info)), None)
#     time.sleep(1)
#     return index_basic_info
#
#
# def insert_new_data(index_basic_info):
#     index_basic_info["list_date"] = index_basic_info["list_date"].apply(convert_str_to_datetime)
#
#     index_basic_info.to_sql("index_basic_info", engine, index=False, if_exists="append")


# def start(market="SW"):
#     delete_old_data()
#     index_basic_info = get_index_basic_info(market)
#     insert_new_data(index_basic_info)


if __name__ == "__main__":
    pass
    # start()
    a = 1
    index_basic_data = pro.index_basic(market="801003.SI")
    print(index_basic_data)
    pass
