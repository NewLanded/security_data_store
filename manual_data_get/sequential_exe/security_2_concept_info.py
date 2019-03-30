import time

import pandas as pd
import tushare as ts

from conf import PRO_KEY
from util_base.db_util import store_data, engine

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def delete_old_data():
    sql = """
    truncate table security_concept_info_detail
    """
    store_data(sql)


def get_security_concept_info():
    security_concept_info = pro.concept(src='ts')
    security_concept_info_detail = pd.DataFrame(columns=["ts_code", "name", "concept_code", "concept_name", "src"])
    for index, row in security_concept_info.iterrows():
        code, name, src = row["code"], row["name"], row["src"]
        security_concept_info_detail_now = pro.concept_detail(id=code, fields='ts_code, name')
        security_concept_info_detail_now["concept_code"] = code
        security_concept_info_detail_now["concept_name"] = name
        security_concept_info_detail_now["src"] = src
        security_concept_info_detail = security_concept_info_detail.append(security_concept_info_detail_now, ignore_index=True)
        time.sleep(2)

    return security_concept_info_detail


def insert_new_data(security_concept_info_detail):
    security_concept_info_detail.to_sql("security_concept_info_detail", engine, index=False, if_exists="append")


def start():
    delete_old_data()

    security_concept_info_detail = get_security_concept_info()
    insert_new_data(security_concept_info_detail)


if __name__ == "__main__":
    start()
