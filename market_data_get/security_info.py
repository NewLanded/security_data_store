import tushare as ts

from conf import PRO_KEY
from util_base.date_util import convert_str_to_datetime
from util_base.db_util import store_data, engine
import time
import datetime
import calendar
ts.set_token(PRO_KEY)
pro = ts.pro_api()


def delete_old_data():
    sql = """
    truncate table s_info
    """
    store_data(sql)


def get_stock_info():
    stock_info = pro.stock_basic(list_status='L')
    time.sleep(3)
    return stock_info


def insert_new_data(s_info_data):
    s_info_data.rename(columns={"symbol": "code"}, inplace=True)
    s_info_data["list_date_new"] = s_info_data["list_date"].apply(convert_str_to_datetime)
    s_info_data.pop("list_date")
    s_info_data.rename(columns={"list_date_new": "list_date"}, inplace=True)

    s_info_data.to_sql("s_info", engine, index=False, if_exists="append")


def start():
    date_now = datetime.datetime.now()
    end_day = calendar.monthrange(date_now.year, date_now.month)[1]
    if date_now.day == end_day:
        delete_old_data()

        stock_info = get_stock_info()
        insert_new_data(stock_info)

    # delete_old_data()
    # stock_info = get_stock_info()
    # insert_new_data(stock_info)


if __name__ == "__main__":
    start()
