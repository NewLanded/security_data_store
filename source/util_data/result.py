import datetime

from source.util_table_module.result_module import BS_Data
from source.util_base.db_util import get_connection


class Result:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def get_unsent_result(self):
        result = self._session.query(BS_Data.id, BS_Data.code, BS_Data.b_point, BS_Data.s_point, BS_Data.quantity, BS_Data.tactics_code).filter(
            BS_Data.sent_flag == 1).all()
        unsent_result = []
        for result_id, code, b_point, s_point, quantity, tactics_code in result:
            unsent_result.append({
                "id": result_id,
                "code": code,
                "b_point": b_point,
                "s_point": s_point,
                "quantity": quantity,
                "tactics_code": tactics_code,
            })
        return unsent_result

    def update_sent_result_flag(self, result_id_list):
        self._session.query(BS_Data).filter(BS_Data.id.in_(result_id_list)).update({"sent_flag": 0}, synchronize_session=False)
        self._session.commit()


if __name__ == "__main__":
    ss = Result()
    print(ss.update_sent_result_flag([1]))
