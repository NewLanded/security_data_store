import datetime
from sqlalchemy import distinct
from source.util_table_module.result_module import BS_Data, Tactics_Success_Rate
from source.util_base.db_util import get_connection
from sqlalchemy import desc


class Result:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def get_all_tactics_code(self):
        result = self._session.query(distinct(BS_Data.tactics_code)).all()
        all_tactics_code = [i[0] for i in result]

        return all_tactics_code

    def get_tactics_success_rate_data_by_date(self, start_date, end_date):
        result = self._session.query(Tactics_Success_Rate.id, Tactics_Success_Rate.tactics_code, Tactics_Success_Rate.raise_sec_num,
                                     Tactics_Success_Rate.forecast_date, Tactics_Success_Rate.all_sec_num, Tactics_Success_Rate.raise_percent,
                                     Tactics_Success_Rate.success_rate_3_day, Tactics_Success_Rate.success_rate_5_day, Tactics_Success_Rate.success_rate_7_day,
                                     Tactics_Success_Rate.gain_loss_3_day, Tactics_Success_Rate.gain_loss_5_day, Tactics_Success_Rate.gain_loss_7_day).filter(
            Tactics_Success_Rate.forecast_date >= start_date, Tactics_Success_Rate.forecast_date <= end_date).all()
        tactics_success_rate_data = {}
        for result_id, tactics_code, raise_sec_num, forecast_date, all_sec_num, raise_percent, success_rate_3_day, success_rate_5_day, success_rate_7_day, gain_loss_3_day, gain_loss_5_day, gain_loss_7_day in result:
            tactics_success_rate_data.setdefault(forecast_date, {})[tactics_code] = {
                "id": result_id,
                "tactics_code": tactics_code,
                "raise_sec_num": raise_sec_num,
                "all_sec_num": all_sec_num,
                "raise_percent": raise_percent,
                "success_rate_3_day": success_rate_3_day,
                "success_rate_5_day": success_rate_5_day,
                "success_rate_7_day": success_rate_7_day,
                "gain_loss_3_day": gain_loss_3_day,
                "gain_loss_5_day": gain_loss_5_day,
                "gain_loss_7_day": gain_loss_7_day
            }

        return tactics_success_rate_data

    def get_unsent_result(self):
        result = self._session.query(BS_Data.id, BS_Data.code, BS_Data.b_point, BS_Data.s_point, BS_Data.quantity, BS_Data.tactics_code,
                                     BS_Data.forecast_date).filter(BS_Data.sent_flag == 0).all()
        unsent_result = []
        for result_id, code, b_point, s_point, quantity, tactics_code, forecast_date in result:
            unsent_result.append({
                "id": result_id,
                "code": code,
                "b_point": b_point,
                "s_point": s_point,
                "quantity": quantity,
                "tactics_code": tactics_code,
                "forecast_date": forecast_date
            })
        return unsent_result

    def get_bs_result_by_forecast(self, start_date, end_date):
        result = self._session.query(BS_Data.id, BS_Data.code, BS_Data.b_point, BS_Data.s_point, BS_Data.quantity, BS_Data.tactics_code,
                                     BS_Data.forecast_date).filter(BS_Data.forecast_date >= start_date, BS_Data.forecast_date <= end_date).all()
        blank_forecast_point_result = {}
        for result_id, code, b_point, s_point, quantity, tactics_code, forecast_date in result:
            blank_forecast_point_result.setdefault(forecast_date, {}).setdefault(tactics_code, []).append({
                "id": result_id,
                "code": code,
                "b_point": b_point,
                "s_point": s_point,
                "quantity": quantity,
            })

        return blank_forecast_point_result

    def update_sent_result_flag(self, result_id_list, sent_flag):
        self._session.query(BS_Data).filter(BS_Data.id.in_(result_id_list)).update({"sent_flag": sent_flag}, synchronize_session=False)
        self._session.commit()

    def get_tactics_code_newest_success_rate(self, tactics_code, date):
        result = self._session.query(Tactics_Success_Rate.id, Tactics_Success_Rate.success_rate_3_day,
                                     Tactics_Success_Rate.success_rate_5_day, Tactics_Success_Rate.success_rate_7_day,
                                     Tactics_Success_Rate.gain_loss_3_day, Tactics_Success_Rate.gain_loss_5_day,
                                     Tactics_Success_Rate.gain_loss_7_day).filter(Tactics_Success_Rate.tactics_code == tactics_code,
                                                                                  Tactics_Success_Rate.forecast_date <= date).order_by(
            desc(Tactics_Success_Rate.forecast_date)).one()
        if result:
            tactics_code_success_rate = {
                "id": result.id,
                "success_rate_3_day": result.success_rate_3_day,
                "success_rate_5_day": result.success_rate_5_day,
                "success_rate_7_day": result.success_rate_7_day,
                "gain_loss_3_day": result.gain_loss_3_day,
                "gain_loss_5_day": result.gain_loss_5_day,
                "gain_loss_7_day": result.gain_loss_7_day
            }
        else:
            tactics_code_success_rate = {}

        return tactics_code_success_rate


if __name__ == "__main__":
    ss = Result()
    print(ss.get_tactics_code_newest_success_rate("1111", datetime.datetime(2019, 10, 11)))
    a = 1
