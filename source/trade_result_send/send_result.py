import datetime

from source.util_data.result import Result
from source.util_module.email_module import send_email


def send_bs_result():
    date_now = datetime.datetime.now()
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

    space_mark = "&nbsp;&nbsp;"

    unsent_result = Result().get_unsent_result()
    for result_dict in unsent_result:
        tactics_code = result_dict["tactics_code"]
        tactics_code_success_rate = Result().get_tactics_code_newest_success_rate(tactics_code, date_now)
        tactics_break_ori_point_success_rate = Result().get_tactics_code_newest_break_success_rate(tactics_code, date_now)

        result_dict["success_rate_3_day"] = tactics_code_success_rate.get("success_rate_3_day", 0)
        result_dict["success_rate_5_day"] = tactics_code_success_rate.get("success_rate_5_day", 0)
        result_dict["success_rate_7_day"] = tactics_code_success_rate.get("success_rate_7_day", 0)
        result_dict["gain_loss_3_day"] = tactics_code_success_rate.get("gain_loss_3_day", 0)
        result_dict["gain_loss_5_day"] = tactics_code_success_rate.get("gain_loss_5_day", 0)
        result_dict["gain_loss_7_day"] = tactics_code_success_rate.get("gain_loss_7_day", 0)
        result_dict["break_in_3_day_rate_avg_7_day"] = tactics_break_ori_point_success_rate.get("break_in_3_day_rate_avg_7_day", 0)
        result_dict["break_in_5_day_rate_avg_7_day"] = tactics_break_ori_point_success_rate.get("break_in_5_day_rate_avg_7_day", 0)
        result_dict["break_in_7_day_rate_avg_7_day"] = tactics_break_ori_point_success_rate.get("break_in_7_day_rate_avg_7_day", 0)
    unsent_result.sort(key=lambda x: [x["success_rate_7_day"], x["success_rate_5_day"], x["success_rate_3_day"]], reverse=True)

    unsent_result_str = "为了确保旅客人身安全和列车运行秩序，车站将在开车时间之前提前停止售票、检票，请合理安排出行时间，提前到乘车站办理换票、安检、验证并到指定场所候车，以免耽误乘车<br>"
    unsent_result_str += "code".ljust(10, " ") + "b_point".ljust(10, " ") + "s_point".ljust(10, " ") + "quantity".ljust(10, " ") + "tactics_code".ljust(
        25) + "success_rate_3_day".ljust(20, " ") + "success_rate_5_day".ljust(20, " ") + "success_rate_7_day".ljust(20, " ") + "gain_loss_3_day".ljust(
        20, " ") + "gain_loss_5_day".ljust(20, " ") + "gain_loss_7_day".ljust(20, " ") + "break_in_3_day".ljust(20, " ") + "break_in_5_day".ljust(
        20, " ") + "break_in_7_day".ljust(20, " ") + "<br>"
    result_id = []

    if unsent_result:
        for result_dict in unsent_result:
            result_id.append(result_dict["id"])
            unsent_result_str += str(result_dict["code"]).ljust(10, " ") + str(result_dict["b_point"]).ljust(10, " ") + str(
                result_dict["s_point"]).ljust(10, " ") + str(
                result_dict["quantity"]).ljust(10, " ") + str(result_dict["tactics_code"]).ljust(25, " ") + str(
                result_dict["success_rate_3_day"]).ljust(20, " ") + str(result_dict["success_rate_5_day"]).ljust(20, " ") + str(
                result_dict["success_rate_7_day"]).ljust(20, " ") + str(result_dict["gain_loss_3_day"]).ljust(20, " ") + str(
                result_dict["gain_loss_5_day"]).ljust(20, " ") + str(result_dict["gain_loss_7_day"]).ljust(20, " ") + str(
                result_dict["break_in_3_day_rate_avg_7_day"]).ljust(20, " ") + str(result_dict["break_in_5_day_rate_avg_7_day"]).ljust(20, " ") + str(
                result_dict["break_in_7_day_rate_avg_7_day"]).ljust(20, " ") + "<br>"

        unsent_result_str = unsent_result_str.replace(" ", space_mark)
        send_email("bs", unsent_result_str)
        Result().update_sent_result_flag(result_id, 1)


if __name__ == "__main__":
    send_bs_result()
