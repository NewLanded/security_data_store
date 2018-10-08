import datetime

import tushare as ts

from source.conf import PRO_KEY
from source.util_base.db_util import get_connection, store_failed_message
from source.util_table_module.base_info_module import S_Info, Security_Status

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_stock_info():
    stock_info = pro.stock_basic(list_status='L', fields='ts_code, symbol, name')
    return stock_info


def store_stock_info(session, stock_info):
    for index, security_info in stock_info.iterrows():
        new_data = S_Info(ts_code=security_info["ts_code"], code=security_info["symbol"], name=security_info["name"],
                          update_date=datetime.datetime.now())
        session.add(new_data)
        session.commit()


def store_stock_status(session, stock_info):
    for index, security_info in stock_info.iterrows():
        normal_status = 0 if "ST" in security_info["name"] else 1
        tactics_1_status = 0 if "ST" in security_info["name"] else 1
        tactics_2_status = 0 if "ST" in security_info["name"] else 1
        tactics_3_status = 0 if "ST" in security_info["name"] else 1
        tactics_4_status = 0 if "ST" in security_info["name"] else 1
        tactics_5_status = 0 if "ST" in security_info["name"] else 1
        tactics_6_status = 0 if "ST" in security_info["name"] else 1
        tactics_7_status = 0 if "ST" in security_info["name"] else 1
        tactics_8_status = 0 if "ST" in security_info["name"] else 1
        tactics_9_status = 0 if "ST" in security_info["name"] else 1
        tactics_10_status = 0 if "ST" in security_info["name"] else 1
        tactics_11_status = 0 if "ST" in security_info["name"] else 1
        tactics_12_status = 0 if "ST" in security_info["name"] else 1
        tactics_13_status = 0 if "ST" in security_info["name"] else 1
        tactics_14_status = 0 if "ST" in security_info["name"] else 1
        tactics_15_status = 0 if "ST" in security_info["name"] else 1
        tactics_16_status = 0 if "ST" in security_info["name"] else 1
        tactics_17_status = 0 if "ST" in security_info["name"] else 1
        tactics_18_status = 0 if "ST" in security_info["name"] else 1
        tactics_19_status = 0 if "ST" in security_info["name"] else 1
        tactics_20_status = 0 if "ST" in security_info["name"] else 1
        new_data = Security_Status(ts_code=security_info["ts_code"],
                                   normal_status=normal_status, tactics_1_status=tactics_1_status,
                                   tactics_2_status=tactics_2_status, tactics_3_status=tactics_3_status,
                                   tactics_4_status=tactics_4_status, tactics_5_status=tactics_5_status,
                                   tactics_6_status=tactics_6_status, tactics_7_status=tactics_7_status,
                                   tactics_8_status=tactics_8_status, tactics_9_status=tactics_9_status,
                                   tactics_10_status=tactics_10_status, tactics_11_status=tactics_11_status,
                                   tactics_12_status=tactics_12_status, tactics_13_status=tactics_13_status,
                                   tactics_14_status=tactics_14_status, tactics_15_status=tactics_15_status,
                                   tactics_16_status=tactics_16_status, tactics_17_status=tactics_17_status,
                                   tactics_18_status=tactics_18_status, tactics_19_status=tactics_19_status,
                                   tactics_20_status=tactics_20_status
                                   )
        session.add(new_data)
        session.commit()


def start():
    session = get_connection()

    try:
        stock_info = get_stock_info()
        store_stock_info(session, stock_info)
        store_stock_status(session, stock_info)
    except Exception as e:
        session.rollback()
        store_failed_message(session, None, "000001", str(e), datetime.date.today())
    session.close()


if __name__ == "__main__":
    start()
