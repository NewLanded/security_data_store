import datetime

from source.util_base.db_util import get_connection
from source.util_data.result import Result
from source.util_table_module.result_module import Tactics_Success_Rate


def get_bs_result(tactics_code, start_date, end_date):
    bs_result_ori = Result().get_bs_result_by_date(tactics_code, start_date, end_date)
    bs_result = {}
    for bs_data in bs_result_ori:
        if bs_data["raise_flag"] is not None:
            bs_result.setdefault(bs_data["forecast_date"], []).append({
                "raise_flag": 1 if bs_data["raise_flag"] is True else 0,
                "raise_pct_change": bs_data["raise_pct_change"]
            })
    return bs_result


def get_tactics_success_rate_dates(bs_result):
    bs_dates = list(bs_result)
    bs_dates.sort(reverse=True)

    bs_result_3_day_dates = bs_dates[0:3]
    bs_result_5_day_dates = bs_dates[0:5]
    bs_result_7_day_dates = bs_dates[0:7]
    bs_result_1_month_dates = bs_dates[0:22]
    bs_result_3_month_dates = bs_dates[0:66]
    bs_result_6_month_dates = bs_dates[0:132]
    bs_result_12_month_dates = bs_dates[0:264]

    return bs_result_3_day_dates, bs_result_5_day_dates, bs_result_7_day_dates, bs_result_1_month_dates, bs_result_3_month_dates, bs_result_6_month_dates, bs_result_12_month_dates


def format_bs_result_list_by_dates(bs_result):
    bs_result_3_day_dates, bs_result_5_day_dates, bs_result_7_day_dates, bs_result_1_month_dates, bs_result_3_month_dates, bs_result_6_month_dates, bs_result_12_month_dates = get_tactics_success_rate_dates(
        bs_result)
    bs_result_3_day, bs_result_5_day, bs_result_7_day, bs_result_1_month, bs_result_3_month, bs_result_6_month, bs_result_12_month = [], [], [], [], [], [], []
    for forecast_date, date_value in bs_result.items():
        for one_date_value in date_value:
            if forecast_date in bs_result_3_day_dates:
                bs_result_3_day.append([one_date_value["raise_flag"], one_date_value["raise_pct_change"]])
            if forecast_date in bs_result_5_day_dates:
                bs_result_5_day.append([one_date_value["raise_flag"], one_date_value["raise_pct_change"]])
            if forecast_date in bs_result_7_day_dates:
                bs_result_7_day.append([one_date_value["raise_flag"], one_date_value["raise_pct_change"]])
            if forecast_date in bs_result_1_month_dates:
                bs_result_1_month.append([one_date_value["raise_flag"], one_date_value["raise_pct_change"]])
            if forecast_date in bs_result_3_month_dates:
                bs_result_3_month.append([one_date_value["raise_flag"], one_date_value["raise_pct_change"]])
            if forecast_date in bs_result_6_month_dates:
                bs_result_6_month.append([one_date_value["raise_flag"], one_date_value["raise_pct_change"]])
            if forecast_date in bs_result_12_month_dates:
                bs_result_12_month.append([one_date_value["raise_flag"], one_date_value["raise_pct_change"]])

    return bs_result_3_day, bs_result_5_day, bs_result_7_day, bs_result_1_month, bs_result_3_month, bs_result_6_month, bs_result_12_month


def calc_tactics_success_rate(bs_result_3_day, bs_result_5_day, bs_result_7_day, bs_result_1_month, bs_result_3_month, bs_result_6_month, bs_result_12_month):
    success_rate = {
        "success_rate_3_day": len([i for i in bs_result_3_day if i[0] == 1]) / len(bs_result_3_day) if len(bs_result_3_day) > 0 else 0,
        "success_rate_5_day": len([i for i in bs_result_5_day if i[0] == 1]) / len(bs_result_5_day) if len(bs_result_5_day) > 0 else 0,
        "success_rate_7_day": len([i for i in bs_result_7_day if i[0] == 1]) / len(bs_result_7_day) if len(bs_result_7_day) > 0 else 0,
        "success_rate_1_month": len([i for i in bs_result_1_month if i[0] == 1]) / len(bs_result_1_month) if len(bs_result_1_month) > 0 else 0,
        "success_rate_3_month": len([i for i in bs_result_3_month if i[0] == 1]) / len(bs_result_3_month) if len(bs_result_3_month) > 0 else 0,
        "success_rate_6_month": len([i for i in bs_result_6_month if i[0] == 1]) / len(bs_result_6_month) if len(bs_result_6_month) > 0 else 0,
        "success_rate_12_month": len([i for i in bs_result_12_month if i[0] == 1]) / len(bs_result_12_month) if len(bs_result_12_month) > 0 else 0
    }
    gain_loss = {
        "gain_loss_3_day": sum([i[1] for i in bs_result_3_day if i[1] is not None]),
        "gain_loss_5_day": sum([i[1] for i in bs_result_5_day if i[1] is not None]),
        "gain_loss_7_day": sum([i[1] for i in bs_result_7_day if i[1] is not None]),
        "gain_loss_1_month": sum([i[1] for i in bs_result_1_month if i[1] is not None]),
        "gain_loss_3_month": sum([i[1] for i in bs_result_3_month if i[1] is not None]),
        "gain_loss_6_month": sum([i[1] for i in bs_result_6_month if i[1] is not None]),
        "gain_loss_12_month": sum([i[1] for i in bs_result_12_month if i[1] is not None])
    }

    return success_rate, gain_loss


def update_tactics_success_rate():
    session = get_connection()
    date_now = datetime.datetime.now()
    start_date, end_date = date_now - datetime.timedelta(days=365), date_now

    all_tactics_code = Result().get_all_tactics_code()
    for tactics_code in all_tactics_code:
        bs_result = get_bs_result(tactics_code, start_date, end_date)
        bs_result_3_day, bs_result_5_day, bs_result_7_day, bs_result_1_month, bs_result_3_month, bs_result_6_month, bs_result_12_month = format_bs_result_list_by_dates(
            bs_result)
        success_rate, gain_loss = calc_tactics_success_rate(bs_result_3_day, bs_result_5_day, bs_result_7_day, bs_result_1_month, bs_result_3_month,
                                                            bs_result_6_month, bs_result_12_month)

        session.query(Tactics_Success_Rate).filter(Tactics_Success_Rate.tactics_code == tactics_code).delete()
        session.commit()

        new_data = Tactics_Success_Rate(tactics_code=tactics_code, success_rate_3_day=success_rate["success_rate_3_day"],
                                        success_rate_5_day=success_rate["success_rate_5_day"], success_rate_7_day=success_rate["success_rate_7_day"],
                                        success_rate_1_month=success_rate["success_rate_1_month"], success_rate_3_month=success_rate["success_rate_3_month"],
                                        success_rate_6_month=success_rate["success_rate_6_month"], success_rate_12_month=success_rate["success_rate_12_month"],
                                        gain_loss_3_day=gain_loss["gain_loss_3_day"], gain_loss_5_day=gain_loss["gain_loss_5_day"],
                                        gain_loss_7_day=gain_loss["gain_loss_7_day"], gain_loss_1_month=gain_loss["gain_loss_1_month"],
                                        gain_loss_3_month=gain_loss["gain_loss_3_month"], gain_loss_6_month=gain_loss["gain_loss_6_month"],
                                        gain_loss_12_month=gain_loss["gain_loss_12_month"],
                                        update_date=datetime.datetime.now())
        session.add(new_data)
        session.commit()


if __name__ == "__main__":
    update_tactics_success_rate()
