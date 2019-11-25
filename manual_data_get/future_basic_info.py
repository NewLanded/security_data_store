import datetime

import tushare as ts

from conf import PRO_KEY

ts.set_token(PRO_KEY)
pro = ts.pro_api()


def name_filter(name, name_shrt):
    if name.startswith(name_shrt):
        if '主力' in name:
            return True
        elif '连续' in name:
            return True
        elif int(name[-4:-2]) >= int(str(datetime.datetime.now().year)[-2:]):
            return True
        else:
            return False
    else:
        return False


def start():
    name_short = ['螺纹钢', '鸡蛋', '豆粕']
    dominant_contract_code_list = ['RB.SHF', 'JD.DCE', 'M.DCE']

    # 查看合约信息
    # 交易所代码 CFFEX-中金所 DCE-大商所 CZCE-郑商所 SHFE-上期所 INE-上海国际能源交易中心
    # 合约类型 (1 普通合约 2主力与连续合约 默认取全部)
    for exchange in ['CFFEX', 'DCE', 'CZCE', 'SHFE', 'INE']:
        df = pro.fut_basic(exchange=exchange, fut_type=None, fields='ts_code,symbol,name,fut_code')
        for name_short_now in name_short:
            df_now = df[df["name"].apply(name_filter, name_shrt=name_short_now)]
            if not df_now.empty:
                df_now = df_now.sort_values(by="name")
                print(df_now)

    # 查看主力合约
    print("\n\n\n\n", "查看主力合约")
    for dominant_contract_code in dominant_contract_code_list:
        df = pro.fut_mapping(ts_code=dominant_contract_code)
        df_now = df[df["trade_date"] == datetime.datetime.now().strftime("%Y%m%d")]
        print(df_now)

    print(pro.fut_mapping(trade_date='20191125'))


if __name__ == "__main__":
    start()
