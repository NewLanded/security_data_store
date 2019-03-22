import datetime


def convert_datetime_to_str(date):
    return date.strftime('%Y%m%d')


def convert_str_to_datetime(date):
    if "-" in date:
        return datetime.datetime.strptime(date, "%Y-%m-%d")
    else:
        return datetime.datetime.strptime(date, "%Y%m%d")


def get_date_range(start_date, end_date):
    date_range = []
    date_now = start_date
    while date_now <= end_date:
        date_range.append(date_now)
        date_now += datetime.timedelta(days=1)

    return date_range
