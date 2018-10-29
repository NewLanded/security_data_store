def start():
    ts_code_open_point_list = [  # code, 开盘价, 持仓成本
        ["000812", 0, 0],
        ["002175", 0, 0],
        ["002622", 0, 0],
        ["000659", 0, 0]
    ]
    for ts_code, open_point, hold_cost in ts_code_open_point_list:
        print(ts_code, open_point * 0.96, hold_cost * 1.07)


if __name__ == "__main__":
    start()