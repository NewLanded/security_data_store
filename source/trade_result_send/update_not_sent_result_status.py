import datetime

from source.util_data.result import Result


def update_not_sent_result_status():
    date_now = datetime.datetime.now()
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    not_relate_to_success_rate_tactics_code = ["fluctuation_tactics_1"]

    unsent_result = Result().get_unsent_result()

    not_send_result_id = []
    if unsent_result:
        for result_dict in unsent_result:
            tactics_code = result_dict["tactics_code"]
            tactics_code_success_rate = Result().get_tactics_code_newest_success_rate(tactics_code, date_now)
            if tactics_code_success_rate.get("success_rate_3_day", 0) >= 0.8 or tactics_code_success_rate.get("success_rate_5_day", 0) >= 0.75 or \
                    tactics_code_success_rate.get("success_rate_7_day", 0) >= 0.7:
                continue
            elif tactics_code in not_relate_to_success_rate_tactics_code:
                continue
            else:
                not_send_result_id.append(result_dict["id"])

        Result().update_sent_result_flag(not_send_result_id, 2)


if __name__ == "__main__":
    update_not_sent_result_status()
