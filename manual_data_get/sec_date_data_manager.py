import datetime

from util_base.date_util import get_date_range
from util_base.db_util import store_data

holiday_manual = {
    datetime.datetime(2016, 1, 1),
    datetime.datetime(2016, 1, 2),
    datetime.datetime(2016, 1, 3),
    datetime.datetime(2016, 2, 7),
    datetime.datetime(2016, 2, 8),
    datetime.datetime(2016, 2, 9),
    datetime.datetime(2016, 2, 10),
    datetime.datetime(2016, 2, 11),
    datetime.datetime(2016, 2, 12),
    datetime.datetime(2016, 2, 13),
    datetime.datetime(2016, 4, 2),
    datetime.datetime(2016, 4, 3),
    datetime.datetime(2016, 4, 4),
    datetime.datetime(2016, 4, 30),
    datetime.datetime(2016, 5, 1),
    datetime.datetime(2016, 5, 2),
    datetime.datetime(2016, 6, 9),
    datetime.datetime(2016, 6, 10),
    datetime.datetime(2016, 6, 11),
    datetime.datetime(2016, 9, 15),
    datetime.datetime(2016, 9, 16),
    datetime.datetime(2016, 9, 17),
    datetime.datetime(2016, 10, 1),
    datetime.datetime(2016, 10, 2),
    datetime.datetime(2016, 10, 3),
    datetime.datetime(2016, 10, 4),
    datetime.datetime(2016, 10, 5),
    datetime.datetime(2016, 10, 6),
    datetime.datetime(2016, 10, 7),
    datetime.datetime(2016, 12, 31),
    datetime.datetime(2017, 1, 1),
    datetime.datetime(2017, 1, 2),
    datetime.datetime(2017, 1, 27),
    datetime.datetime(2017, 1, 28),
    datetime.datetime(2017, 1, 29),
    datetime.datetime(2017, 1, 30),
    datetime.datetime(2017, 1, 31),
    datetime.datetime(2017, 2, 1),
    datetime.datetime(2017, 2, 2),
    datetime.datetime(2017, 4, 2),
    datetime.datetime(2017, 4, 3),
    datetime.datetime(2017, 4, 4),
    datetime.datetime(2017, 4, 29),
    datetime.datetime(2017, 4, 30),
    datetime.datetime(2017, 5, 1),
    datetime.datetime(2017, 5, 28),
    datetime.datetime(2017, 5, 29),
    datetime.datetime(2017, 5, 30),
    datetime.datetime(2017, 10, 1),
    datetime.datetime(2017, 10, 2),
    datetime.datetime(2017, 10, 3),
    datetime.datetime(2017, 10, 4),
    datetime.datetime(2017, 10, 5),
    datetime.datetime(2017, 10, 6),
    datetime.datetime(2017, 10, 7),
    datetime.datetime(2017, 10, 8),
    datetime.datetime(2017, 10, 9),
    datetime.datetime(2017, 10, 10),
    datetime.datetime(2017, 12, 30),
    datetime.datetime(2017, 12, 31),
    datetime.datetime(2018, 1, 1),
    datetime.datetime(2018, 2, 15),
    datetime.datetime(2018, 2, 16),
    datetime.datetime(2018, 2, 17),
    datetime.datetime(2018, 2, 18),
    datetime.datetime(2018, 2, 19),
    datetime.datetime(2018, 2, 20),
    datetime.datetime(2018, 2, 21),
    datetime.datetime(2018, 4, 5),
    datetime.datetime(2018, 4, 6),
    datetime.datetime(2018, 4, 7),
    datetime.datetime(2018, 4, 29),
    datetime.datetime(2018, 5, 1),
    datetime.datetime(2018, 6, 16),
    datetime.datetime(2018, 6, 17),
    datetime.datetime(2018, 6, 18),
    datetime.datetime(2018, 9, 22),
    datetime.datetime(2018, 9, 23),
    datetime.datetime(2018, 9, 24),
    datetime.datetime(2018, 10, 1),
    datetime.datetime(2018, 10, 2),
    datetime.datetime(2018, 10, 3),
    datetime.datetime(2018, 10, 4),
    datetime.datetime(2018, 10, 5),
    datetime.datetime(2018, 10, 6),
    datetime.datetime(2018, 10, 7),
    datetime.datetime(2019, 1, 1),
    datetime.datetime(2019, 1, 2),
    datetime.datetime(2019, 2, 4),
    datetime.datetime(2019, 2, 5),
    datetime.datetime(2019, 2, 6),
    datetime.datetime(2019, 2, 7),
    datetime.datetime(2019, 2, 8),
    datetime.datetime(2019, 4, 5),
    datetime.datetime(2019, 5, 1),
    datetime.datetime(2019, 5, 2),
    datetime.datetime(2019, 5, 3),
    datetime.datetime(2019, 6, 7),
    datetime.datetime(2019, 9, 13),
    datetime.datetime(2019, 10, 1),
    datetime.datetime(2019, 10, 2),
    datetime.datetime(2019, 10, 3),
    datetime.datetime(2019, 10, 4),
    datetime.datetime(2019, 10, 7),
    datetime.datetime(2020, 1, 1),
    datetime.datetime(2020, 1, 24),
    datetime.datetime(2020, 1, 27),
    datetime.datetime(2020, 1, 28),
    datetime.datetime(2020, 1, 29),
    datetime.datetime(2020, 1, 30),
    datetime.datetime(2020, 1, 31),
    datetime.datetime(2020, 4, 6),
    datetime.datetime(2020, 5, 1),
    datetime.datetime(2020, 5, 4),
    datetime.datetime(2020, 5, 5),
    datetime.datetime(2020, 6, 25),
    datetime.datetime(2020, 6, 26),
    datetime.datetime(2020, 10, 1),
    datetime.datetime(2020, 10, 2),
    datetime.datetime(2020, 10, 5),
    datetime.datetime(2020, 10, 6),
    datetime.datetime(2020, 10, 7),
    datetime.datetime(2020, 10, 8),
}


def delete_old_data():
    sql = """
    truncate table sec_date_info
    """
    store_data(sql)


def insert_new_data(date, is_workday_flag):
    sql = """
    insert into sec_date_info(date, is_workday_flag) values(:date, :is_workday_flag)
    """
    args = {"date": date, "is_workday_flag": is_workday_flag}
    store_data(sql, args)


def start():
    start_date = datetime.datetime(2016, 1, 1)
    end_date = datetime.datetime(2020, 12, 31)

    date_range = get_date_range(start_date, end_date)

    delete_old_data()

    for date in date_range:
        is_workday_flag = 1 if datetime.datetime.isoweekday(date) <= 5 and date not in holiday_manual else 0
        insert_new_data(date, is_workday_flag)


if __name__ == "__main__":
    start()
