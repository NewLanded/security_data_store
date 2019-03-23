import datetime
import time

import tushare as ts

from conf import PRO_KEY
from util_base.date_util import convert_datetime_to_str, convert_str_to_datetime
from util_base.db_util import engine
from util_base.db_util import store_failed_message
from util_data.date import Date
from util_data.stock import Stock

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_qfq_security_point_data(ts_code):
    time.sleep(1)
    qfq_security_point_data = ts.pro_bar(pro_api=pro, ts_code=ts_code, adj='qfq', start_date='20160101', end_date='20190323')
    time.sleep(1)
    return qfq_security_point_data


def store_security_point_data(qfq_security_point_data):
    qfq_security_point_data["update_date"] = datetime.datetime.now()
    qfq_security_point_data["trade_date"] = qfq_security_point_data["trade_date"].apply(convert_str_to_datetime)
    qfq_security_point_data["pct_chg"] = qfq_security_point_data["pct_chg"].apply(lambda x: x / 100)

    qfq_security_point_data.to_sql("qfq_security_point_data", engine, index=False, if_exists="append")


def start():
    stocks_info = Stock().get_all_stocks_info()
    for ts_code, ts_code_info in stocks_info.items():
        qfq_security_point_data = get_qfq_security_point_data(ts_code)
        store_security_point_data(qfq_security_point_data)


if __name__ == "__main__":
    pass
    start()
    # all_security_point_data = ts.pro_bar(pro_api=pro, ts_code='002195.SZ', adj='qfq', start_date='20180101', end_date='20181011')
    # a = 1
    pass
