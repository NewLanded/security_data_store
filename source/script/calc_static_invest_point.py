from source.util_base.db_util import get_connection
from source.util_module.email_module import send_email
from source.util_table_module.result_module import Static_Invest


def get_send_code_info():
    session = get_connection()
    send_code_info = session.query(Static_Invest.ts_code, Static_Invest.name, Static_Invest.open_point, Static_Invest.hold_cost, Static_Invest.buy_percent,
                                   Static_Invest.sell_percent).filter(Static_Invest.sent_flag == 0).all()
    session.close()
    return send_code_info


def format_result(result_data):
    space_mark = "&nbsp;&nbsp;"
    result_str = "为了确保旅客人身安全和列车运行秩序，车站将在开车时间之前提前停止售票、检票，请合理安排出行时间，提前到乘车站办理换票、安检、验证并到指定场所候车，以免耽误乘车<br>"
    result_str += "code".ljust(10, " ") + "name".ljust(10, " ") + "buy_point".ljust(10, " ") + "sell_point".ljust(10, " ") + "<br>"

    for ts_code, name, buy_point, sell_point in result_data:
        result_str += ts_code.ljust(10, " ") + name.ljust(10, " ") + str(buy_point).ljust(10, " ") + str(sell_point).ljust(10, " ") + "<br>"
    result_str = result_str.replace(" ", space_mark)
    return result_str


def update_send_flag():
    session = get_connection()
    send_code_info = session.query(Static_Invest).update({"sent_flag": 1}, synchronize_session=False)
    session.commit()
    session.close()
    return send_code_info


def calc_static_invest_point():
    send_code_info = get_send_code_info()
    if send_code_info:
        update_send_flag()

        result_data = []
        for ts_code, name, open_point, hold_cost, buy_percent, sell_percent in send_code_info:  # code, nema, 开盘价, 持仓成本
            if hold_cost == 0:
                buy_point = round(open_point * buy_percent, 3)
            else:
                buy_point = round(open_point * buy_percent if open_point * buy_percent < hold_cost else hold_cost, 3)
            sell_point = round(hold_cost * sell_percent, 3)

            result_data.append([ts_code, name, buy_point, sell_point])

        result_str = format_result(result_data)

        send_email("static_invest", result_str)


if __name__ == "__main__":
    calc_static_invest_point()
