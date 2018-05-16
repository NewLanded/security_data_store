import datetime

import tushare as ts

from source.moudle.base_info_moudle import S_Info
from source.moudle.data_moudle import Hs300_Rehabilitation_Data
from source.util.date_util import convert_datetime_to_str
from source.util.db_util import get_connection, store_failed_message


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


if __name__ == "__main__":
    session = get_connection()

    codes = get_codes(session)
    start_date, end_date = datetime.datetime(2018, 5, 1), datetime.datetime(2018, 5, 16)
    # start_date, end_date = datetime.datetime.now(), datetime.datetime.now()
    load_dates = []
    for code in codes:
        try:
            hs300_rehabilitation_data = get_hs300_rehabilitation_data(code, convert_datetime_to_str(start_date),
                                                                      convert_datetime_to_str(end_date))
            store_hs300_rehabilitation_data(session, code, hs300_rehabilitation_data)
        except Exception as e:
            store_failed_message(session, code, "000002", str(e), None)
    session.close()
