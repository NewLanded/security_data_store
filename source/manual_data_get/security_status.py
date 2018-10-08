import datetime

from source.util_base.db_util import get_connection, store_failed_message
from source.util_data.stock import Stock
from source.util_table_module.base_info_module import Security_Status


def get_security_point_data(ts_code, date_now):
    pass


def calc_tactics_1_status(security_daily_basic_data):
    turnover_rate_list = [data["turnover_rate"] for data in security_daily_basic_data.values() if data["turnover_rate"] is not None]
    average_turnover_rate = sum(turnover_rate_list) / len(turnover_rate_list)
    if average_turnover_rate >= 0.07:
        return True
    else:
        return False


def store_stock_status(session, ts_code, ts_code_info, security_point_data, security_daily_basic_data):
    normal_status = 0 if "ST" in ts_code_info["name"] else 1  # ST股为0
    tactics_1_status = 0 if calc_tactics_1_status(security_daily_basic_data) is False else 1  # 换手率小于0.07的为0, 差不多300条
    tactics_2_status = None
    tactics_3_status = None
    tactics_4_status = None
    tactics_5_status = None
    tactics_6_status = None
    tactics_7_status = None
    tactics_8_status = None
    tactics_9_status = None
    tactics_10_status = None
    tactics_11_status = None
    tactics_12_status = None
    tactics_13_status = None
    tactics_14_status = None
    tactics_15_status = None
    tactics_16_status = None
    tactics_17_status = None
    tactics_18_status = None
    tactics_19_status = None
    tactics_20_status = None
    new_data = Security_Status(ts_code=ts_code,
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


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    session = get_connection()

    try:
        stocks_info = Stock().get_all_stocks_info()
        for ts_code, ts_code_info in stocks_info.items():
            security_point_data = get_security_point_data(ts_code, date_now)
            security_daily_basic_data = Stock().get_security_daily_basic_data(ts_code, date_now - datetime.timedelta(days=30), date_now)

            store_stock_status(session, ts_code, ts_code_info, security_point_data, security_daily_basic_data)
    except Exception as e:
        session.rollback()
        store_failed_message(session, None, "000001", str(e), datetime.date.today())
    session.close()


if __name__ == "__main__":
    start()
    # session = get_connection()
