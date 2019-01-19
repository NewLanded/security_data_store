import datetime

from source.util_base.db_util import get_connection
from source.util_data.date import Date
from source.util_data.result import Result
from source.util_data.stock import Stock
from source.util_table_module.result_module import Tactics_Break_Ori_Point_Success_Rate


def store_tactics_break_ori_point_success_num(session, break_ori_point_sec_num_in_3_day, break_ori_point_sec_num_in_5_day, break_ori_point_sec_num_in_7_day,
                                              all_sec_num, date_now, tactics_code):
    new_data = Tactics_Break_Ori_Point_Success_Rate(tactics_code=tactics_code, forecast_date=date_now,
                                                    break_ori_point_sec_num_in_3_day=break_ori_point_sec_num_in_3_day,
                                                    break_ori_point_sec_num_in_5_day=break_ori_point_sec_num_in_5_day,
                                                    break_ori_point_sec_num_in_7_day=break_ori_point_sec_num_in_7_day, all_sec_num=all_sec_num,
                                                    update_date=datetime.datetime.now())
    session.add(new_data)
    session.commit()


def calc_break_data(date_previous_7_day_security_point_data, security_point_data):
    open_point = date_previous_7_day_security_point_data["open"]
    open_point_raise_one_percent = open_point + open_point * 0.01

    date_list = list(security_point_data)
    date_list.sort()

    break_3_day_dates, break_5_day_dates, break_7_day_dates = date_list[:3], date_list[:5], date_list[:7]
    break_3_day_flag, break_5_day_flag, break_7_day_flag = 0, 0, 0
    for date, date_value in security_point_data.items():
        if date in break_3_day_dates and date_value["high"] > open_point_raise_one_percent:
            break_3_day_flag = 1
        if date in break_5_day_dates and date_value["high"] > open_point_raise_one_percent:
            break_5_day_flag = 1
        if date in break_7_day_dates and date_value["high"] > open_point_raise_one_percent:
            break_7_day_flag = 1

    return break_3_day_flag, break_5_day_flag, break_7_day_flag


def update_tactics_break_ori_point_success_num(date_now):
    if Date().is_workday(date_now):
        session = get_connection()
        all_stocks_info = Stock().get_all_stocks_info()
        code_ts_code_map = dict([[ts_code_info['code'], ts_code] for ts_code, ts_code_info in all_stocks_info.items()])

        date_previous_8_day = Date().get_previous_n_workday(date_now, 8)
        if date_previous_8_day:
            date_previous_8_day = date_previous_8_day[0]

            bs_result = Result().get_bs_result_by_forecast(date_previous_8_day, date_previous_8_day).get(date_previous_8_day, {})
            for tactics_code, tactics_code_value_list in bs_result.items():
                break_ori_point_sec_num_in_3_day, break_ori_point_sec_num_in_5_day, break_ori_point_sec_num_in_7_day, all_sec_num = 0, 0, 0, 0
                for one_code_data in tactics_code_value_list:
                    if one_code_data["bs_flag"] == "b":
                        security_point_data = Stock().get_security_point_data(code_ts_code_map[one_code_data["code"]], date_previous_8_day, date_now)
                        if date_previous_8_day in security_point_data:
                            date_previous_8_day_security_point_data = security_point_data.pop(date_previous_8_day)
                        else:
                            continue

                        break_ori_point_sec_num_in_3_day_now, break_ori_point_sec_num_in_5_day_now, break_ori_point_sec_num_in_7_day_now = calc_break_data(
                            date_previous_8_day_security_point_data, security_point_data)
                        break_ori_point_sec_num_in_3_day += break_ori_point_sec_num_in_3_day_now
                        break_ori_point_sec_num_in_5_day += break_ori_point_sec_num_in_5_day_now
                        break_ori_point_sec_num_in_7_day += break_ori_point_sec_num_in_7_day_now
                        all_sec_num += 1

                store_tactics_break_ori_point_success_num(session, break_ori_point_sec_num_in_3_day, break_ori_point_sec_num_in_5_day,
                                                          break_ori_point_sec_num_in_7_day, all_sec_num, date_now, tactics_code)
        session.close()


if __name__ == "__main__":
    # date_now = datetime.datetime.now()
    # date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)
    date_now = datetime.datetime(2018, 10, 17)
    update_tactics_break_ori_point_success_num(date_now)
