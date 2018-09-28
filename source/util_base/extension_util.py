from source.conf import PRO_KEY
import tushare as ts

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def get_ts_pro():
    return pro
