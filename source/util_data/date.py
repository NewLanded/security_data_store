import datetime

from sqlalchemy.sql import func

from source.util_base.db_util import get_connection
from source.util_table_module.base_info_module import Sec_Date_Info


class Date:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def is_workday(self, date):
        result = self._session.query(Sec_Date_Info).filter(Sec_Date_Info.date == date).one()
        workday_flag = True if result.is_workday_flag == 1 else False
        return workday_flag

    def get_previous_workday(self, date):
        previous_workday = self._session.query(func.max(Sec_Date_Info.date)).filter(Sec_Date_Info.date < date, Sec_Date_Info.is_workday_flag == 1).one()
        if previous_workday:
            previous_workday = previous_workday[0]
        else:
            previous_workday = None

        return previous_workday

    def get_previous_n_workday(self, date, n):
        data_num = 0
        date_now = date
        result = []
        loop_count = 100
        while data_num < n and loop_count:
            start_date = date_now - datetime.timedelta(n * 2)
            result_now = self._session.query(Sec_Date_Info).filter(Sec_Date_Info.date >= start_date, Sec_Date_Info.date <= date_now,
                                                                   Sec_Date_Info.is_workday_flag == 1).all()
            result.extend(result_now)
            date_now = start_date
            data_num = len(result)
            loop_count -= 1

        previous_n_workday = []
        for row in result:
            previous_n_workday.append(row.date)
        previous_n_workday.sort()
        previous_n_workday = previous_n_workday[-n:]
        return previous_n_workday


if __name__ == "__main__":
    ss = Date()
    ee = ss.get_previous_workday(datetime.datetime(2018, 10, 9))
    a = 1
