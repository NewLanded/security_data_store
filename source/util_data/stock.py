import datetime

from source.util_table_module.base_info_module import Security_Status, S_Info
from source.util_base.db_util import get_connection
from source.util_table_module.data_module import Security_Daily_Basic, Security_Point_Data


class Stock:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def get_all_stocks_info(self):
        result = self._session.query(S_Info).all()
        stocks_info = {}
        for stock_info in result:
            stocks_info[stock_info.ts_code] = {
                "code": stock_info.code,
                "name": stock_info.name
            }
        return stocks_info

    def get_security_daily_basic_data(self, ts_code, start_date, end_date):
        result = self._session.query(Security_Daily_Basic).filter(Security_Daily_Basic.ts_code == ts_code, Security_Daily_Basic.trade_date >= start_date,
                                                                  Security_Daily_Basic.trade_date <= end_date).all()
        security_daily_basic_data = {}
        for one_day_basic_data in result:
            security_daily_basic_data[one_day_basic_data.trade_date] = {
                "close": one_day_basic_data.close,
                "turnover_rate": one_day_basic_data.turnover_rate / 100 if one_day_basic_data.turnover_rate else one_day_basic_data.turnover_rate,
                "volume_ratio": one_day_basic_data.volume_ratio,
                "pe": one_day_basic_data.pe,
                "pe_ttm": one_day_basic_data.pe_ttm,
                "pb": one_day_basic_data.pb,
                "ps": one_day_basic_data.ps,
                "ps_ttm": one_day_basic_data.ps_ttm,
                "total_share": one_day_basic_data.total_share,
                "float_share": one_day_basic_data.float_share,
                "free_share": one_day_basic_data.free_share,
                "total_mv": one_day_basic_data.total_mv,
                "circ_mv": one_day_basic_data.circ_mv,
            }
        return security_daily_basic_data

    def get_security_point_data(self, ts_code, start_date, end_date):
        result = self._session.query(Security_Point_Data).filter(Security_Point_Data.ts_code == ts_code, Security_Point_Data.trade_date >= start_date,
                                                                 Security_Point_Data.trade_date <= end_date).all()
        security_point_data = {}
        for one_day_point_data in result:
            security_point_data[one_day_point_data.trade_date] = {
                "open": one_day_point_data.open,
                "high": one_day_point_data.high,
                "low": one_day_point_data.low,
                "close": one_day_point_data.close,
                "pre_close": one_day_point_data.pre_close,
                "change": one_day_point_data.change,
                "pct_chg": one_day_point_data.pct_chg / 100,
                "vol": one_day_point_data.vol,
                "amount": one_day_point_data.amount,
            }
        return security_point_data

    def is_valid_security_normal(self, ts_code):
        result = self._session.query(Security_Status).filter(Security_Status.ts_code == ts_code).all()
        valid_flag = True if result and result[0].normal_status == 1 else False
        return valid_flag

    def is_valid_security_tactics_1(self, ts_code):
        result = self._session.query(Security_Status).filter(Security_Status.ts_code == ts_code).all()
        valid_flag = True if result and result[0].normal_status == 1 and result[0].tactics_1_status == 1 else False
        return valid_flag


if __name__ == "__main__":
    ss = Stock()
    aa = ss.get_security_point_data('000001.SZ', datetime.datetime(2018, 7, 1), datetime.datetime(2018, 7, 4))
    print(aa)
    rr = 1
