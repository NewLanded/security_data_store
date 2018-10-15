import datetime
from sqlalchemy import distinct
from source.util_table_module.result_module import BS_Data, Tactics_Success_Rate
from source.util_base.db_util import get_connection


class Result:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def get_all_tactics_code(self):
        result = self._session.query(distinct(BS_Data.tactics_code)).all()
        all_tactics_code = [i[0] for i in result]

        return all_tactics_code

    def get_bs_result_by_date(self, tactics_code, start_date, end_date):
        result = self._session.query(BS_Data.id, BS_Data.code, BS_Data.b_point, BS_Data.s_point, BS_Data.quantity, BS_Data.tactics_code,
                                     BS_Data.forecast_date, BS_Data.raise_flag, BS_Data.raise_pct_change).filter(BS_Data.tactics_code == tactics_code,
                                                                                                                 BS_Data.forecast_date >= start_date,
                                                                                                                 BS_Data.forecast_date <= end_date).all()
        bs_result = []
        for result_id, code, b_point, s_point, quantity, tactics_code, forecast_date, raise_flag, raise_pct_change in result:
            bs_result.append({
                "id": result_id,
                "code": code,
                "b_point": b_point,
                "s_point": s_point,
                "quantity": quantity,
                "tactics_code": tactics_code,
                "forecast_date": forecast_date,
                "raise_flag": raise_flag,
                "raise_pct_change": raise_pct_change
            })

        return bs_result

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

    def get_blank_forecast_point_result(self):
        result = self._session.query(BS_Data.id, BS_Data.code, BS_Data.b_point, BS_Data.s_point, BS_Data.quantity, BS_Data.tactics_code,
                                     BS_Data.forecast_date).filter(BS_Data.raise_flag == None).all()
        blank_forecast_point_result = []
        for result_id, code, b_point, s_point, quantity, tactics_code, forecast_date in result:
            blank_forecast_point_result.append({
                "id": result_id,
                "code": code,
                "b_point": b_point,
                "s_point": s_point,
                "quantity": quantity,
                "tactics_code": tactics_code,
                "forecast_date": forecast_date
            })
        return blank_forecast_point_result

    def update_sent_result_flag(self, result_id_list, sent_flag):
        self._session.query(BS_Data).filter(BS_Data.id.in_(result_id_list)).update({"sent_flag": sent_flag}, synchronize_session=False)
        self._session.commit()

    def update_raise_column(self, result_id, raise_flag, raise_pct_change):
        self._session.query(BS_Data).filter(BS_Data.id == result_id).update({"raise_flag": raise_flag, "raise_pct_change": raise_pct_change},
                                                                            synchronize_session=False)
        self._session.commit()

    def get_tactics_code_success_rate(self):
        result = self._session.query(Tactics_Success_Rate.id, Tactics_Success_Rate.tactics_code, Tactics_Success_Rate.success_rate_3_day,
                                     Tactics_Success_Rate.success_rate_5_day, Tactics_Success_Rate.success_rate_7_day,
                                     Tactics_Success_Rate.success_rate_1_month, Tactics_Success_Rate.success_rate_3_month,
                                     Tactics_Success_Rate.success_rate_6_month, Tactics_Success_Rate.success_rate_12_month,
                                     Tactics_Success_Rate.gain_loss_3_day, Tactics_Success_Rate.gain_loss_5_day,
                                     Tactics_Success_Rate.gain_loss_7_day, Tactics_Success_Rate.gain_loss_1_month,
                                     Tactics_Success_Rate.gain_loss_3_month, Tactics_Success_Rate.gain_loss_6_month,
                                     Tactics_Success_Rate.gain_loss_12_month).all()
        tactics_code_success_rate = {}
        for result_id, tactics_code, success_rate_3_day, success_rate_5_day, success_rate_7_day, success_rate_1_month, success_rate_3_month, success_rate_6_month, success_rate_12_month, gain_loss_3_day, gain_loss_5_day, gain_loss_7_day, gain_loss_1_month, gain_loss_3_month, gain_loss_6_month, gain_loss_12_month in result:
            tactics_code_success_rate[tactics_code] = {
                "id": result_id,
                "success_rate_3_day": success_rate_3_day,
                "success_rate_5_day": success_rate_5_day,
                "success_rate_7_day": success_rate_7_day,
                "success_rate_1_month": success_rate_1_month,
                "success_rate_3_month": success_rate_3_month,
                "success_rate_6_month": success_rate_6_month,
                "success_rate_12_month": success_rate_12_month,
                "gain_loss_3_day": gain_loss_3_day,
                "gain_loss_5_day": gain_loss_5_day,
                "gain_loss_7_day": gain_loss_7_day,
                "gain_loss_1_month": gain_loss_1_month,
                "gain_loss_3_month": gain_loss_3_month,
                "gain_loss_6_month": gain_loss_6_month,
                "gain_loss_12_month": gain_loss_12_month,
            }
        return tactics_code_success_rate


if __name__ == "__main__":
    ss = Result()
    print(ss.get_bs_result_by_date("fluctuation_tactics_1", datetime.datetime(2018, 10, 11), datetime.datetime(2018, 10, 11)))
