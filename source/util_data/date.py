import datetime

from source.moudle.base_info_moudle import Sec_Date_Info
from source.util_base.db_util import get_connection


class Date:
    def __init__(self):
        self.session = get_connection()
    
    def __del__(self):
        self.session.close()

    def is_workday(self, date):
        result = self.session.query(Sec_Date_Info).filter(Sec_Date_Info.date == date).one()
        workday_flag = True if result.is_workday_flag == 1 else False
        return workday_flag


if __name__ == "__main__":
    ss = Date()
    ss.is_workday(datetime.datetime(2018, 9, 7))
