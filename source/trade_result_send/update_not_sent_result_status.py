from source.util_data.result import Result


def update_not_sent_result_status():
    not_relate_to_success_rate_tactics_code = ["fluctuation_tactics_1"]

    unsent_result = Result().get_unsent_result()
    tactics_code_success_rate = Result().get_tactics_code_success_rate()

    not_send_result_id = []
    if unsent_result:
        for result_dict in unsent_result:
            tactics_code = result_dict["tactics_code"]
            if tactics_code_success_rate.get(tactics_code, {}).get("success_rate_3_day", 0) == 1 or tactics_code_success_rate.get(tactics_code, {}).get(
                    "success_rate_5_day", 0) >= 0.8 or tactics_code_success_rate.get(tactics_code, {}).get("success_rate_7_day", 0) >= 0.85:
                continue
            elif tactics_code in not_relate_to_success_rate_tactics_code:
                pass
            else:
                not_send_result_id.append(result_dict["id"])

        Result().update_sent_result_flag(not_send_result_id, 2)


if __name__ == "__main__":
    update_not_sent_result_status()
