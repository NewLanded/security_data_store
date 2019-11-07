from util_base.db_util import get_multi_data, update_data


class Market:
    def get_holder_number_data(self, ts_code, start_date, end_date):
        sql = """
        select ts_code, ann_date, end_date, holder_num from holder_number_data where ts_code = :ts_code and ann_date >= :start_date and ann_date <= :end_date
        """
        args = {"ts_code": ts_code, "start_date": start_date, "end_date": end_date}
        result = get_multi_data(sql, args)
        holder_number_data = []
        for ts_code, ann_date, end_date, holder_num in result:
            holder_number_data.append({
                "ann_date": ann_date,
                "end_date": end_date,
                "holder_num": holder_num
            })
        return holder_number_data

    def delete_holder_number_data(self, ts_code, start_date, end_date):
        sql = """
        delete from holder_number_data where ts_code = :ts_code and ann_date >= :start_date and ann_date <= :end_date
        """
        args = {"ts_code": ts_code, "start_date": start_date, "end_date": end_date}
        update_data(sql, args)
