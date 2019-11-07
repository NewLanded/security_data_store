import datetime

import pandas as pd

from util_base.db_util import engine
from util_base.db_util import store_data
from util_data.stock import Stock


def delete_old_data():
    sql = """
    truncate table security_status
    """
    store_data(sql)


def calc_tactics_1_status(security_daily_basic_data):
    turnover_rate_list = [data["turnover_rate"] for data in security_daily_basic_data.values() if data["turnover_rate"] is not None]

    if not turnover_rate_list:
        return False

    average_turnover_rate = sum(turnover_rate_list) / len(turnover_rate_list)
    if average_turnover_rate >= 0.07:
        return True
    else:
        return False


def calc_tactics_2_status(security_daily_basic_data):
    turnover_rate_list = [data["turnover_rate"] for data in security_daily_basic_data.values() if data["turnover_rate"] is not None]

    if not turnover_rate_list:
        return False

    average_turnover_rate = sum(turnover_rate_list) / len(turnover_rate_list)
    if average_turnover_rate >= 0.03:
        return True
    else:
        return False


def calc_tactics_3_status(security_daily_basic_data):
    free_share_list = [data["free_share"] for data in security_daily_basic_data.values() if data["free_share"] is not None]

    if not free_share_list:
        return False

    average_free_share = sum(free_share_list) / len(free_share_list)
    if average_free_share >= 50000:
        return True
    else:
        return False


def calc_tactics_4_status(security_daily_basic_data):
    share_ratio_list = [data["free_share"] / data["total_share"] for data in security_daily_basic_data.values() if
                        data["free_share"] is not None and data["total_share"]]

    if not share_ratio_list:
        return False

    average_share_ratio = sum(share_ratio_list) / len(share_ratio_list)
    if average_share_ratio >= 0.6:
        return True
    else:
        return False


def calc_tactics_5_status(code):
    if code.startswith("600"):
        return True
    elif code.startswith("601"):
        return True
    elif code.startswith("603"):
        return True
    elif code.startswith("000"):
        return True
    elif code.startswith("002"):
        return True
    else:
        return False


def calc_tactics_6_status(security_point_data):
    security_point_data_date = list(security_point_data)
    security_point_data_date.sort()
    security_point_data_date = security_point_data_date[-550:]

    if len(security_point_data_date) < 550:
        return True

    previous_index = 0
    previous_avg_point = None
    compare_lesser_number = 0
    for index in range(50, 551, 50):
        security_point_data_date_now = security_point_data_date[previous_index: index]

        avg_point = sum(security_point_data[i]["close"] for i in security_point_data_date_now) / len(security_point_data_date_now)

        if previous_avg_point is None:
            pass
        else:
            if avg_point < previous_avg_point:
                compare_lesser_number += 1

        previous_index = index
        previous_avg_point = avg_point

    if compare_lesser_number >= 8:
        return False
    else:
        return True


def calc_tactics_7_status(security_point_data):
    security_point_data_date = list(security_point_data)
    security_point_data_date.sort()
    security_point_data_date = security_point_data_date[-550:]

    if len(security_point_data_date) < 550:
        return True

    previous_index = 0
    previous_avg_point = None
    compare_lesser_number = 0
    for index in range(50, 551, 50):
        security_point_data_date_now = security_point_data_date[previous_index: index]

        avg_point = sum(security_point_data[i]["close"] for i in security_point_data_date_now) / len(security_point_data_date_now)

        if previous_avg_point is None:
            pass
        else:
            if avg_point < previous_avg_point:
                compare_lesser_number += 1

        previous_index = index
        previous_avg_point = avg_point

    if compare_lesser_number >= 7:
        return False
    else:
        return True


def calc_stock_status(ts_code, date_now, ts_code_info):
    security_daily_basic_data = Stock().get_security_daily_basic_data(ts_code, date_now - datetime.timedelta(days=90), date_now)
    security_point_data = Stock().get_security_point_data(ts_code, date_now - datetime.timedelta(days=1000), date_now)

    result = {
        "ts_code": ts_code,
        "normal_status": 0 if "ST" in ts_code_info["name"] else 1,  # ST股为0
        "tactics_1_status": 0 if calc_tactics_1_status(security_daily_basic_data) is False else 1,  # 换手率大于等于0.07的为1, 差不多300条, 这应该都是一些小股票
        "tactics_2_status": 0 if calc_tactics_2_status(security_daily_basic_data) is False else 1,  # 换手率大于等于0.03的为1, 差不多900条, 应该包含了一些中大型股票
        "tactics_3_status": 0 if calc_tactics_3_status(security_daily_basic_data) is False else 1,  # 流通股本大于等于50000, 差不多1000条
        "tactics_4_status": 0 if calc_tactics_4_status(security_daily_basic_data) is False else 1,  # 流通股本 / 总股本 大于等于0.6, 差不多714条
        "tactics_5_status": 0 if calc_tactics_5_status(ts_code_info["code"]) is False else 1,  # 深证A股, 上证A股, 中小板 为1
        "tactics_6_status": 0 if calc_tactics_6_status(security_point_data) is False else 1,  # 找过去550天的数据, 分成11份, 取平均值, 若有8份及以上, 是较前一份数据在跌的, 认为这个个券不可靠, 设置为0
        "tactics_7_status": 0 if calc_tactics_7_status(security_point_data) is False else 1,  # 找过去550天的数据, 分成11份, 取平均值, 若有7份及以上, 是较前一份数据在跌的, 认为这个个券不可靠, 设置为0,
        "tactics_8_status": None,
        "tactics_9_status": None,
        "tactics_10_status": None,
        "tactics_11_status": None,
        "tactics_12_status": None,
        "tactics_13_status": None,
        "tactics_14_status": None,
        "tactics_15_status": None,
        "tactics_16_status": None,
        "tactics_17_status": None,
        "tactics_18_status": None,
        "tactics_19_status": None,
        "tactics_20_status": None
    }

    return result


def calc_status_info(date_now, stocks_info):
    status_info = []
    for ts_code, ts_code_info in stocks_info.items():
        result_now = calc_stock_status(ts_code, date_now, ts_code_info)
        status_info.append(result_now)
    return status_info


def store_result(status_info):
    status_dataframe = pd.DataFrame(status_info, columns=[
        "ts_code", "normal_status", "tactics_1_status", "tactics_2_status", "tactics_3_status", "tactics_4_status", "tactics_5_status", "tactics_6_status", "tactics_7_status",
        "tactics_8_status", "tactics_9_status", "tactics_10_status", "tactics_11_status", "tactics_12_status", "tactics_13_status", "tactics_14_status", "tactics_15_status",
        "tactics_16_status", "tactics_17_status", "tactics_18_status", "tactics_19_status", "tactics_20_status",
    ])
    status_dataframe.to_sql("security_status", engine, index=False, if_exists="append")


def start(date_now=None):
    date_now = datetime.datetime.now() if date_now is None else date_now
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    delete_old_data()
    stocks_info = Stock().get_all_stocks_info()
    status_info = calc_status_info(date_now, stocks_info)
    store_result(status_info)


if __name__ == "__main__":
    start()
