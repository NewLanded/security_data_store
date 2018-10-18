import datetime

from source.util_base.db_util import get_connection
from source.util_data.result import Result
from source.util_data.stock import Stock
from source.util_table_module.result_module import Tactics_Success_Rate


def store_sactics_success_rate(session, raise_sec_num, all_sec_num, raise_percent, date_now, tactics_code):
    new_data = Tactics_Success_Rate(tactics_code=tactics_code, forecast_date=date_now, raise_sec_num=raise_sec_num, all_sec_num=all_sec_num,
                                    raise_percent=raise_percent, update_date=datetime.datetime.now())
    session.add(new_data)
    session.commit()


def update_tactics_success_num(date_now):
    session = get_connection()
    all_stocks_info = Stock().get_all_stocks_info()
    code_ts_code_map = dict([[ts_code_info['code'], ts_code] for ts_code, ts_code_info in all_stocks_info.items()])

    bs_result = Result().get_bs_result_by_forecast(date_now, date_now).get(date_now, {})
    for tactics_code, tactics_code_value_list in bs_result.items():
        raise_sec_num, all_sec_num, raise_percent = 0, 0, 0
        for one_code_data in tactics_code_value_list:
            security_pct_change = Stock().get_security_point_data(code_ts_code_map[one_code_data["code"]], date_now, date_now).get(date_now, {}).get(
                "pct_change", None)
            if security_pct_change and security_pct_change > 0:
                raise_sec_num += 1
            all_sec_num += 1
            raise_percent += security_pct_change
        store_sactics_success_rate(session, raise_sec_num, all_sec_num, raise_percent, date_now, tactics_code)
    session.close()


if __name__ == "__main__":
    # date_now = datetime.datetime.now()
    # date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)
    date_now = datetime.datetime(2018, 10, 17)
    update_tactics_success_num(date_now)
