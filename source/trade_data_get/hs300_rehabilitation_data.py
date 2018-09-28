import datetime
import logging
import tushare as ts

from source.util_table_module.base_info_module import S_Info
from source.util_table_module.data_module import Hs300_Rehabilitation_Data
from source.util_base.date_util import convert_datetime_to_str
from source.util_base.db_util import get_connection, store_failed_message
from source.util_data.date import Date

logger = logging.getLogger('/home/stock/app/security_data_store/timed_task.hs300_rehabilitation_data')


def get_codes(session):
    codes = session.query(S_Info.code).all()
    codes = [i[0] for i in codes]
    return codes


def get_hs300_rehabilitation_data(code, start_date_str, end_date_str):
    hs300_rehabilitation_data = ts.get_k_data(code, start=start_date_str, end=end_date_str)
    return hs300_rehabilitation_data


def store_hs300_rehabilitation_data(session, code, hs300_rehabilitation_data):
    for index, data in hs300_rehabilitation_data.iterrows():
        new_data = Hs300_Rehabilitation_Data(code=code, date=data["date"], open=data["open"], high=data["high"],
                                             close=data["close"], low=data["low"], volume=data["volume"],
                                             update_date=datetime.datetime.now())
        session.add(new_data)
        session.commit()


def start():
    session = get_connection()

    # date_now = datetime.datetime(2018, 9, 14)
    date_now = datetime.datetime.now()
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)
    date_now_previous_day = date_now - datetime.timedelta(days=1)

    if Date().is_workday(date_now_previous_day):
        codes = get_codes(session)
        start_date, end_date = date_now_previous_day, date_now_previous_day
        for code in codes:
            try:
                hs300_rehabilitation_data = get_hs300_rehabilitation_data(code, convert_datetime_to_str(start_date),
                                                                          convert_datetime_to_str(end_date))
                store_hs300_rehabilitation_data(session, code, hs300_rehabilitation_data)
            except Exception as e:
                store_failed_message(session, code, "000002", str(e), None)
    session.close()


if __name__ == "__main__":
    start()
