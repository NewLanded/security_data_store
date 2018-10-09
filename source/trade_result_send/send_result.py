from source.util_data.result import Result
from source.util_module.email_module import send_email


def send_bs_result():
    unsent_result = Result().get_unsent_result()
    unsent_result_str = "感谢您成为谷歌上网助手会员，你的本次支付的信息如下\n"
    unsent_result_str += "code".ljust(10) + "b_point".ljust(10) + "s_point".ljust(10) + "quantity".ljust(10) + "tactics_code".ljust(20) + "\r\n"
    result_id = []

    if unsent_result:
        for result_dict in unsent_result:
            result_id.append(result_dict["id"])
            unsent_result_str += str(result_dict["code"]).ljust(10) + str(result_dict["b_point"]).ljust(10) + str(result_dict["s_point"]).ljust(10) + str(
                result_dict["quantity"]).ljust(10) + str(result_dict["tactics_code"]).ljust(20) + "\r\n"

        send_email("bs", unsent_result_str)
        Result().update_sent_result_flag(result_id)


if __name__ == "__main__":
    send_bs_result()
