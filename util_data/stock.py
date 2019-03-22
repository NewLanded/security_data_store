import datetime

from util_base.db_util import get_multi_data


class Stock:
    def get_all_stocks_info(self):
        sql = """
        select ts_code, code, name from s_info
        """
        result = get_multi_data(sql)
        stocks_info = {}
        for ts_code, code, name in result:
            stocks_info[ts_code] = {
                "code": code,
                "name": name
            }
        return stocks_info

    def get_security_daily_basic_data(self, ts_code, start_date, end_date):
        sql = """
        select `trade_date`, `close`, `turnover_rate`, `turnover_rate_f`, `volume_ratio`, `pe`, `pe_ttm`, `pb`, `ps`, `ps_ttm`, `total_share`, `float_share`, `free_share`, `total_mv`, `circ_mv` from security_daily_basic
        where ts_code = :ts_code and trade_date >= :start_date and trade_date <= :end_date
        """
        args = {"ts_code": ts_code, "start_date": start_date, "end_date": end_date}
        result = get_multi_data(sql, args)

        security_daily_basic_data = {}
        for trade_date, close, turnover_rate, turnover_rate_f, volume_ratio, pe, pe_ttm, pb, ps, ps_ttm, total_share, float_share, free_share, total_mv, circ_mv in result:
            security_daily_basic_data[trade_date] = {
                "close": close,
                "turnover_rate": turnover_rate,
                "turnover_rate_f": turnover_rate_f,
                "volume_ratio": volume_ratio,
                "pe": pe,
                "pe_ttm": pe_ttm,
                "pb": pb,
                "ps": ps,
                "ps_ttm": ps_ttm,
                "total_share": total_share,
                "float_share": float_share,
                "free_share": free_share,
                "total_mv": total_mv,
                "circ_mv": circ_mv,
            }
        return security_daily_basic_data

    def get_security_point_data(self, ts_code, start_date, end_date):
        sql = """
        select `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount` from security_point_data
        where ts_code = :ts_code and trade_date >= :start_date and trade_date <= :end_date
        """
        args = {"ts_code": ts_code, "start_date": start_date, "end_date": end_date}
        result = get_multi_data(sql, args)

        security_point_data = {}
        for trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount in result:
            security_point_data[trade_date] = {
                "open": open,
                "high": high,
                "low": low,
                "close": close,
                "pre_close": pre_close,
                "change": change,
                "pct_chg": pct_chg,
                "vol": vol,
                "amount": amount,
            }
        return security_point_data


if __name__ == "__main__":
    ss = Stock()
    aa = ss.get_security_point_data('000001.SZ', datetime.datetime(2018, 7, 1), datetime.datetime(2018, 7, 4))
    print(aa)
    rr = 1
