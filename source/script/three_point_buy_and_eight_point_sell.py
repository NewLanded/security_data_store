import datetime

from source.util_data.stock import Stock

if __name__ == "__main__":
    ts_code_list = ['600720.SH', '000509.SZ', '002460.SZ', '600216.SH', '002405.SZ', '002161.SZ', '600326.SH', '000735.SZ', '002526.SZ', '000650.SZ',
                    '600711.SH', '002023.SZ', '600495.SH', '000636.SZ', '002195.SZ', '000528.SZ', '002554.SZ', '000812.SZ', '600130.SH', '002463.SZ',
                    '000401.SZ', '000407.SZ', '000506.SZ', '000830.SZ', '002175.SZ', '000979.SZ', '002259.SZ', '600856.SH', '002622.SZ', '000793.SZ',
                    '002447.SZ', '600596.SH']
    result_data = []
    for ts_code in ts_code_list:
        security_point_data_ori = Stock().get_security_point_data(ts_code, datetime.datetime(2018, 6, 1), datetime.datetime(2018, 10, 1))
        security_point_data = []
        for date, date_value in security_point_data_ori.items():
            security_point_data.append([date, date_value["high"], date_value["low"], date_value["open"]])
        security_point_data.sort(key=lambda x: x[0])

        hold_cost = None
        success_date = []
        total_hand = 0
        for date, high, low, open_point in security_point_data:
            if low <= open_point * 0.97 and total_hand <= 15:
                if hold_cost is None:
                    hold_cost = open_point * 0.97
                else:
                    hold_cost = (hold_cost + open_point * 0.97) / 2

                total_hand += 1

            if hold_cost is not None and high > hold_cost * 1.08:
                success_date.append(date)
                hold_cost = None
                total_hand = 0
        result_data.append([ts_code, len(success_date)])
    result_data.sort(key=lambda x: x[1], reverse=True)
    print(result_data)
