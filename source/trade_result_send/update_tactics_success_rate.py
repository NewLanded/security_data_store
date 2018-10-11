import datetime

from source.util_base.db_util import get_connection
from source.util_data.result import Result
from source.util_table_module.result_module import Tactics_Success_Rate


def update_tactics_success_rate():
    session = get_connection()
    date_now = datetime.datetime.now()
    start_date, end_date = date_now - datetime.timedelta(days=365), date_now

    all_tactics_code = Result().get_all_tactics_code()
    for tactics_code in all_tactics_code:
        bs_result = Result().get_bs_result_by_date(tactics_code, start_date, end_date)
        bs_result = [[bs_data["forecast_date"], 1 if bs_data["raise_flag"] is True else 0] for bs_data in bs_result if bs_data["raise_flag"] is not None]
        bs_result.sort(key=lambda x: x[0])

        bs_result_3_day = bs_result[-3:]
        bs_result_5_day = bs_result[-5:]
        bs_result_7_day = bs_result[-7:]
        success_rate_1_month = bs_result[-30:]
        success_rate_3_month = bs_result[-90:]
        success_rate_6_month = bs_result[-180:]
        success_rate_12_month = bs_result[:]

        success_rate_3_day = len([i for i in bs_result_3_day if i[1] == 1]) / len(bs_result_3_day) if len(bs_result_3_day) > 0 else 0
        success_rate_5_day = len([i for i in bs_result_5_day if i[1] == 1]) / len(bs_result_5_day) if len(bs_result_5_day) > 0 else 0
        success_rate_7_day = len([i for i in bs_result_7_day if i[1] == 1]) / len(bs_result_7_day) if len(bs_result_7_day) > 0 else 0
        success_rate_1_month = len([i for i in success_rate_1_month if i[1] == 1]) / len(success_rate_1_month) if len(success_rate_1_month) > 0 else 0
        success_rate_3_month = len([i for i in success_rate_3_month if i[1] == 1]) / len(success_rate_3_month) if len(success_rate_3_month) > 0 else 0
        success_rate_6_month = len([i for i in success_rate_6_month if i[1] == 1]) / len(success_rate_6_month) if len(success_rate_6_month) > 0 else 0
        success_rate_12_month = len([i for i in success_rate_12_month if i[1] == 1]) / len(success_rate_12_month) if len(success_rate_12_month) > 0 else 0

        session.query(Tactics_Success_Rate).filter(Tactics_Success_Rate.tactics_code == tactics_code).delete()
        session.commit()

        new_data = Tactics_Success_Rate(tactics_code=tactics_code, success_rate_3_day=success_rate_3_day, success_rate_5_day=success_rate_5_day,
                                        success_rate_7_day=success_rate_7_day,
                                        success_rate_1_month=success_rate_1_month, success_rate_3_month=success_rate_3_month,
                                        success_rate_6_month=success_rate_6_month, success_rate_12_month=success_rate_12_month,
                                        update_date=datetime.datetime.now())
        session.add(new_data)
        session.commit()


if __name__ == "__main__":
    update_tactics_success_rate()
