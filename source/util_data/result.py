import datetime

from source.module.result_module import BS_Data
from source.util_base.db_util import get_connection


class Result:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def get_unsent_result(self):
        result = self._session.query(BS_Data.code, BS_Data.b_point, BS_Data.s_point, BS_Data.quantity, BS_Data.tactics_code).filter(BS_Data.sent_flag == 1).all()
        unsent_result = []
        for code, b_point, s_point, quantity, tactics in result:
            unsent_result.append({
                "code": code,
                "b_point": b_point,
                "s_point": s_point,
                "quantity": quantity,
                "tactics": tactics,
            })
        return unsent_result


if __name__ == "__main__":
    ss = Result()
    print(ss.get_unsent_result())
