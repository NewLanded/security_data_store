import datetime

from source.util_base.db_util import get_connection
from source.util_data.result import Result
from source.util_table_module.result_module import Tactics_Break_Ori_Point_Success_Rate


def format_tactics_break_ori_point_success_rate_data(tactics_break_ori_point_success_rate_data):
    tactics_break_ori_point_success_rate_data_new = {}
    for date, date_value in tactics_break_ori_point_success_rate_data.items():
        for tactics_code, tactics_code_value in date_value.items():
            tactics_break_ori_point_success_rate_data_new.setdefault(tactics_code, {})[date] = tactics_code_value

    return tactics_break_ori_point_success_rate_data_new


def get_tactics_break_ori_point_success_data_by_dates(tactics_code_value):
    tactics_success_dates = list(tactics_code_value)
    tactics_success_dates.sort(reverse=True)

    tactics_success_result_dates = tactics_success_dates[0:7]

    tactics_success_result_3_day_data, tactics_success_result_5_day_data, tactics_success_result_7_day_data, all_sec_num_data = [], [], [], []
    for date, date_value in tactics_code_value.items():
        if date in tactics_success_result_dates:
            tactics_success_result_3_day_data.append(date_value["break_ori_point_sec_num_in_3_day"])
            tactics_success_result_5_day_data.append(date_value["break_ori_point_sec_num_in_5_day"])
            tactics_success_result_7_day_data.append(date_value["break_ori_point_sec_num_in_7_day"])
            all_sec_num_data.append(date_value["all_sec_num"])

    return tactics_success_result_3_day_data, tactics_success_result_5_day_data, tactics_success_result_7_day_data, all_sec_num_data


def calc_tactics_success_rate(break_in_3_day_data, break_in_5_day_data, break_in_7_day_data, all_sec_num_data):
    if sum(all_sec_num_data) == 0:
        return {
            "break_in_3_day_rate_avg_7_day": 0,
            "break_in_5_day_rate_avg_7_day": 0,
            "break_in_7_day_rate_avg_7_day": 0,
        }

    success_rate = {
        "break_in_3_day_rate_avg_7_day": sum(break_in_3_day_data) / sum(all_sec_num_data),
        "break_in_5_day_rate_avg_7_day": sum(break_in_5_day_data) / sum(all_sec_num_data),
        "break_in_7_day_rate_avg_7_day": sum(break_in_7_day_data) / sum(all_sec_num_data)
    }
    return success_rate


def update_tactics_break_ori_point_success_rate_result(session, result_id, success_rate):
    session.query(Tactics_Break_Ori_Point_Success_Rate).filter(Tactics_Break_Ori_Point_Success_Rate.id == result_id).update(
        {"break_in_3_day_rate_avg_7_day": success_rate["break_in_3_day_rate_avg_7_day"],
         "break_in_5_day_rate_avg_7_day": success_rate["break_in_5_day_rate_avg_7_day"],
         "break_in_7_day_rate_avg_7_day": success_rate["break_in_7_day_rate_avg_7_day"]}, synchronize_session=False)
    session.commit()


def update_tactics_break_ori_point_success_rate(date_now):
    session = get_connection()
    start_date, end_date = date_now - datetime.timedelta(days=30), date_now

    tactics_break_ori_point_success_rate_data = Result().get_tactics_break_ori_point_success_rate_data_by_date(start_date, end_date)
    tactics_break_ori_point_success_rate_data = format_tactics_break_ori_point_success_rate_data(tactics_break_ori_point_success_rate_data)
    for tactics_code, tactics_code_value in tactics_break_ori_point_success_rate_data.items():
        date_now_tactics_break_ori_point_success_rate_result = tactics_code_value.get(date_now, None)
        if not date_now_tactics_break_ori_point_success_rate_result:
            continue

        break_in_3_day_data, break_in_5_day_data, break_in_7_day_data, all_sec_num_data = get_tactics_break_ori_point_success_data_by_dates(tactics_code_value)
        success_rate = calc_tactics_success_rate(break_in_3_day_data, break_in_5_day_data, break_in_7_day_data, all_sec_num_data)

        update_tactics_break_ori_point_success_rate_result(session, date_now_tactics_break_ori_point_success_rate_result.get("id"), success_rate)

    session.close()


if __name__ == "__main__":
    # date_now = datetime.datetime.now()
    # date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)
    date_now = datetime.datetime(2018, 10, 17)
    update_tactics_break_ori_point_success_rate(date_now)
