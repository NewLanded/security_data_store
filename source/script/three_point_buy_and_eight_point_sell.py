import datetime

from source.util_data.stock import Stock

if __name__ == "__main__":
    ts_code_list = ['600720.SH', '000509.SZ', '002460.SZ', '600216.SH', '002405.SZ', '002161.SZ', '600326.SH', '000735.SZ', '002526.SZ', '000650.SZ',
                    '600711.SH', '002023.SZ', '600495.SH', '000636.SZ', '002195.SZ', '000528.SZ', '002554.SZ', '000812.SZ', '600130.SH', '002463.SZ',
                    '000401.SZ', '000407.SZ', '000506.SZ', '000830.SZ', '002175.SZ', '000979.SZ', '002259.SZ', '600856.SH', '002622.SZ', '000793.SZ',
                    '002447.SZ', '600596.SH']
    result_data = []
    buy_rate = 0.96
    sell_rate = 1.07
    for ts_code in ts_code_list:
        security_point_data_ori = Stock().get_security_point_data(ts_code, datetime.datetime(2018, 6, 1), datetime.datetime(2018, 10, 1))
        security_point_data = []
        for date, date_value in security_point_data_ori.items():
            security_point_data.append([date, date_value["high"], date_value["low"], date_value["open"], date_value["pre_close"]])
        security_point_data.sort(key=lambda x: x[0])

        hold_cost = None
        success_date = []
        section_hand_list = []
        total_hand = 0
        one_section_hand = 0
        for date, high, low, open_point, pre_close in security_point_data:
            if hold_cost is not None and high > hold_cost * sell_rate:  # 不能放下边, 当天买的不能当天卖
                success_date.append(date)
                section_hand_list.append(one_section_hand)
                hold_cost = None
                one_section_hand = 0
                continue

            # if low <= open_point * buy_rate:
            if low <= open_point * buy_rate and (hold_cost is None or open_point * buy_rate <= hold_cost):
                if hold_cost is None:
                    hold_cost = open_point * buy_rate
                else:
                    hold_cost = (hold_cost + open_point * buy_rate) / 2

                total_hand += 1
                one_section_hand += 1

        result_data.append([ts_code, len(success_date), total_hand - one_section_hand, max(section_hand_list) if section_hand_list else None])
    result_data.sort(key=lambda x: [x[2], x[1]], reverse=True)
    result_data = list(filter(lambda x: x[3] is not None and x[3] <= 6, result_data))
    print(result_data)  # 代码, 成功次数, 总买入次数, 每次成功的最大买入次数
