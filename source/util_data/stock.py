import datetime

from source.util_table_module.base_info_module import Security_Status
from source.util_base.db_util import get_connection


class Stock:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

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
    aa = ss.is_valid_security_normal('000001.SZ')
    print(aa)
    rr = 1
