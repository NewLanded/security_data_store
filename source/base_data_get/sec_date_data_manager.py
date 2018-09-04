import datetime

from source.moudle.base_info_moudle import Sec_Date_Info
from source.util.date_util import get_date_range
from source.util.db_util import get_connection


def start():
    session = get_connection()
    start_date = datetime.datetime(2016, 1, 1)
    end_date = datetime.datetime(2050, 12, 31)

    date_range = get_date_range(start_date, end_date)
    for date in date_range:
        is_workday_flag = 1 if datetime.datetime.isoweekday(date) <= 5 else 0
        new_data = Sec_Date_Info(date=date, is_workday_flag=is_workday_flag)
        session.add(new_data)
        session.commit()


if __name__ == "__main__":
    start()
