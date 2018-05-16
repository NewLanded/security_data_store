import datetime

from moudle import Failed_Code


def store_failed_message(session, code, index, error_message, date):
    data = Failed_Code(code=code, index=index, error_message=error_message, date=date,
                       update_date=datetime.datetime.now())
    session.add(data)
    session.commit()


def convert_datetime_to_str(date):
    return date.strftime('%Y-%m-%d')


def convert_str_to_datetime(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d")


def get_date_range(start_date, end_date):
    date_range = []
    date_now = start_date
    while date_now <= end_date:
        date_range.append(date_now)
        date_now += datetime.timedelta(days=1)

    return date_range

# if __name__ == "__main__":
#     print(get_date_range(datetime.datetime(2016, 1, 1), datetime.datetime(2016, 1, 4)))
