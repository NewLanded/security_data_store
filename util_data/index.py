from util_base.db_util import get_multi_data


class Index:
    def get_index_basic_info(self, market):
        sql = """
        select ts_code, name, market, publisher, category, base_date, base_point, list_date from Index_Basic_Info where market = :market
        """
        args = {"market": market}
        result = get_multi_data(sql, args)
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
