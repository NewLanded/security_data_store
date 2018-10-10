from source.util_data.result import Result
from source.util_data.stock import Stock


def update_forecase_point():
    all_stocks_info = Stock().get_all_stocks_info()
    code_ts_code_map = dict([[ts_code_info['code'], ts_code] for ts_code, ts_code_info in all_stocks_info.items()])

    blank_forecast_point_result = Result().get_blank_forecast_point_result()
    for one_blank_forecast_point in blank_forecast_point_result:
        security_pct_change = Stock().get_security_point_data(code_ts_code_map[one_blank_forecast_point["code"]], one_blank_forecast_point["forecast_date"],
                                                              one_blank_forecast_point["forecast_date"]).get(one_blank_forecast_point["forecast_date"], {}).get(
            "pct_change", None)
        raise_flag = 1 if security_pct_change > 0 else 0
        raise_pct_change = security_pct_change

        Result().update_raise_column(one_blank_forecast_point["id"], raise_flag, raise_pct_change)


if __name__ == "__main__":
    update_forecase_point()
