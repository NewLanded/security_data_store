import datetime

from util_base.db_util import get_multi_data


class Date:
    def is_workday(self, date):
        sql = """
        select 1 from sec_date_info where date=:date and is_workday_flag=true
        """
        args = {"date": date}
        result = get_multi_data(sql, args)
        result = True if result else False

        return result

    def get_previous_workday(self, date):
        sql = """
        select max(date) from sec_date_info where date<:date and is_workday_flag=true
        """
        args = {"date": date}
        result = get_multi_data(sql, args)

        if result:
            previous_workday = result[0][0]
        else:
            previous_workday = None

        return previous_workday

    def get_previous_n_workday(self, date, n):
        data_num = 0
        date_now = date
        result = []
        loop_count = 100
        sql = """
        select date from sec_date_info where date<=:date_now and date>:start_date and is_workday_flag=true
        """
        while data_num < n and loop_count:
            start_date = date_now - datetime.timedelta(n * 2)

            args = {"start_date": start_date, "date_now": date_now}
            result_now = get_multi_data(sql, args)
            result.extend(result_now)

            date_now = start_date
            data_num = len(result)
            loop_count -= 1

        previous_n_workday = []
        for row in result:
            previous_n_workday.append(row[0])
        previous_n_workday.sort()
        previous_n_workday = previous_n_workday[-n:]
        return previous_n_workday


if __name__ == "__main__":
    ss = Date()
    ee = ss.get_previous_n_workday(datetime.datetime(2018, 10, 9), 10)
    print(ee)
