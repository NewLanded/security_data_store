def get_send_code_info():
    pass


def start():
    get_send_code_info = get_send_code_info()

    result = []
    for ts_code, name, open_point, hold_cost, buy_percent, sell_percent in get_send_code_info:  # code, nema, 开盘价, 持仓成本
        if hold_cost == 0:
            buy_point = round(open_point * buy_percent, 3)
        else:
            buy_point = round(open_point * buy_percent if open_point * buy_percent < hold_cost else hold_cost, 3)
        sell_cost = round(hold_cost * sell_percent, 3)

        result.append([ts_code, name, buy_point, sell_cost])


    print("code".ljust(10, " "), "name".ljust(10, " "), "buy_point".ljust(10, " "), "sell_point".ljust(10, " "))

    




if __name__ == "__main__":
    start()

"""
CREATE TABLE `static_invest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(12) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `open_point` float DEFAULT NULL,
  `hold_cost` float DEFAULT NULL,
  `buy_percent` float DEFAULT NULL,
  `sell_percent` float DEFAULT NULL,
  `sent_flag` tinyint(1) DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
)


"""