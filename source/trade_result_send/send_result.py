from source.util_data.result import Result
from source.util_module.email_module import send_email


def send_bs_result():
    unsent_result = Result().get_unsent_result()
    unsent_result_str = "为了确保旅客人身安全和列车运行秩序，车站将在开车时间之前提前停止售票、检票，请合理安排出行时间，提前到乘车站办理换票、安检、验证并到指定场所候车，以免耽误乘车<br>"
    unsent_result_str += "code".ljust(10) + "b_point".ljust(10) + "s_point".ljust(10) + "quantity".ljust(10) + "tactics_code".ljust(20) + "<br>"
    result_id = []

    if unsent_result:
        for result_dict in unsent_result:
            result_id.append(result_dict["id"])
            unsent_result_str += str(result_dict["code"]).ljust(10) + str(result_dict["b_point"]).ljust(10) + str(result_dict["s_point"]).ljust(10) + str(
                result_dict["quantity"]).ljust(10) + str(result_dict["tactics_code"]).ljust(20) + "<br>"

        send_email("bs", unsent_result_str)
        Result().update_sent_result_flag(result_id)


if __name__ == "__main__":
    send_bs_result()
