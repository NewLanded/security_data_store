import datetime

from source.util_base.db_util import get_connection
from source.util_data.result import Result
from source.util_table_module.result_module import Tactics_Success_Rate


def format_tactics_success_num_data(tactics_success_num_data):
    tactics_success_num_data_new = {}
    for date, date_value in tactics_success_num_data.items():
        for tactics_code, tactics_code_value in date_value.items():
            tactics_success_num_data_new.setdefault(tactics_code, {})[date] = tactics_code_value

    return tactics_success_num_data_new


def get_tactics_success_data_by_dates(tactics_code_value):
    tactics_success_dates = list(tactics_code_value)
    tactics_success_dates.sort(reverse=True)

    tactics_success_result_3_day_dates = tactics_success_dates[0:3]
    tactics_success_result_5_day_dates = tactics_success_dates[0:5]
    tactics_success_result_7_day_dates = tactics_success_dates[0:7]

    tactics_success_result_3_day_data, tactics_success_result_5_day_data, tactics_success_result_7_day_data = [], [], []
    for date, date_value in tactics_code_value.items():
        if date in tactics_success_result_3_day_dates:
            tactics_success_result_3_day_data.append(date_value)
        if date in tactics_success_result_5_day_dates:
            tactics_success_result_5_day_data.append(date_value)
        if date in tactics_success_result_7_day_dates:
            tactics_success_result_7_day_data.append(date_value)

    return tactics_success_result_3_day_data, tactics_success_result_5_day_data, tactics_success_result_7_day_data


def calc_tactics_success_rate(tactics_success_result_3_day_data, tactics_success_result_5_day_data, tactics_success_result_7_day_data):
    success_rate = {
        "success_rate_3_day": sum([i["raise_sec_num"] for i in tactics_success_result_3_day_data]) / sum(
            [i["all_sec_num"] for i in tactics_success_result_3_day_data]) if sum([i["all_sec_num"] for i in tactics_success_result_3_day_data]) > 0 else 0,
        "success_rate_5_day": sum([i["raise_sec_num"] for i in tactics_success_result_5_day_data]) / sum(
            [i["all_sec_num"] for i in tactics_success_result_5_day_data]) if sum([i["all_sec_num"] for i in tactics_success_result_5_day_data]) > 0 else 0,
        "success_rate_7_day": sum([i["raise_sec_num"] for i in tactics_success_result_7_day_data]) / sum(
            [i["all_sec_num"] for i in tactics_success_result_7_day_data]) if sum([i["all_sec_num"] for i in tactics_success_result_7_day_data]) > 0 else 0
    }
    gain_loss = {
        "gain_loss_3_day": sum([i["raise_percent"] for i in tactics_success_result_3_day_data]),
        "gain_loss_5_day": sum([i["raise_percent"] for i in tactics_success_result_5_day_data]),
        "gain_loss_7_day": sum([i["raise_percent"] for i in tactics_success_result_7_day_data])
    }

    return success_rate, gain_loss


def update_tactics_success_rate_result(session, result_id, success_rate, gain_loss):
    session.query(Tactics_Success_Rate).filter(Tactics_Success_Rate.id == result_id).update(
        {"success_rate_3_day": success_rate["success_rate_3_day"], "success_rate_5_day": success_rate["success_rate_5_day"],
         "success_rate_7_day": success_rate["success_rate_7_day"], "gain_loss_3_day": gain_loss["gain_loss_3_day"],
         "gain_loss_5_day": gain_loss["gain_loss_5_day"], "gain_loss_7_day": gain_loss["gain_loss_7_day"]}, synchronize_session=False)
    session.commit()


def update_tactics_success_rate(date_now):
    session = get_connection()
    start_date, end_date = date_now - datetime.timedelta(days=30), date_now

    tactics_success_num_data = Result().get_tactics_success_rate_data_by_date(start_date, end_date)
    tactics_success_num_data = format_tactics_success_num_data(tactics_success_num_data)
    for tactics_code, tactics_code_value in tactics_success_num_data.items():
        date_now_tactics_success_result = tactics_code_value.get(date_now, None)
        if not date_now_tactics_success_result:
            continue

        tactics_success_result_3_day_data, tactics_success_result_5_day_data, tactics_success_result_7_day_data = get_tactics_success_data_by_dates(
            tactics_code_value)
        success_rate, gain_loss = calc_tactics_success_rate(tactics_success_result_3_day_data, tactics_success_result_5_day_data,
                                                            tactics_success_result_7_day_data)

        update_tactics_success_rate_result(session, date_now_tactics_success_result.get("id"), success_rate, gain_loss)

    session.close()


if __name__ == "__main__":
    # date_now = datetime.datetime.now()
    # date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)
    date_now = datetime.datetime(2018, 10, 17)
    update_tactics_success_rate(date_now)
