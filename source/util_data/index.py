from source.util_base.db_util import get_connection
from source.util_table_module.index_module import Index_Basic_Info


class Index:
    def __init__(self):
        self._session = get_connection()

    def __del__(self):
        self._session.close()

    def get_index_basic_info(self, market):
        result = self._session.query(Index_Basic_Info.ts_code, Index_Basic_Info.name, Index_Basic_Info.market, Index_Basic_Info.publisher,
                                     Index_Basic_Info.category, Index_Basic_Info.base_date, Index_Basic_Info.base_point, Index_Basic_Info.list_date).filter(
                                     Index_Basic_Info.market == market).all()
        index_basic_info = {}
        for ts_index_code, name, market, publisher, category, base_date, base_point, list_date in result:
            index_basic_info[ts_index_code] = {
                "name": name,
                "market": market,
                "publisher": publisher,
                "category": category,
                "base_date": base_date,
                "base_point": base_point,
                "list_date": list_date,
            }

        return index_basic_info


if __name__ == "__main__":
    ss = Index()
    print(ss.get_index_basic_info("SW"))
