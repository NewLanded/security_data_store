import datetime

from source.util_data.stock import Stock

if __name__ == "__main__":
    security_point_data_ori = Stock().get_security_point_data("600999.SH", datetime.datetime(2018, 6, 1), datetime.datetime(2018, 10, 1))
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
    print(success_date)
