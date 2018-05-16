import datetime

import tushare as ts

from db_connection import get_connection
from moudle import S_Info
from util import store_failed_message


def get_hs300_base_data():
    hs300_weight_data = ts.get_hs300s()
    return hs300_weight_data


def store_hs300_base_data(session, hs300_weight_data):
    for index, security_weight_data in hs300_weight_data.iterrows():
        new_data = S_Info(code=security_weight_data["code"], name=security_weight_data["name"],
                          hs300_weight=security_weight_data["weight"], data_date=security_weight_data["date"],
                          update_date=datetime.datetime.now())
        session.add(new_data)
        session.commit()


if __name__ == "__main__":
    session = get_connection()

    try:
        hs300_weight_data = get_hs300_base_data()
        store_hs300_base_data(session, hs300_weight_data)
    except Exception as e:
        store_failed_message(session, None, "000001", str(e), datetime.date.today())
    session.close()