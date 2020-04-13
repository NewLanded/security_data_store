import pdfplumber
import os
import datetime
from util_base.db_util import engine
import pandas as pd
import shutil


def get_spot_price(pdf_path):
    good_name_contract_code_map = {
        '棕榈油': 'P'
    }
    contract_code_price = {}

    with pdfplumber.open(pdf_path) as pdf:
        spot_price_flag = False
        for page in pdf.pages:
            table_data_list = page.extract_table()
            for row in table_data_list:
                if row[0] and '现货价格及价差' in row[0]:
                    spot_price_flag = True

                if spot_price_flag is True:
                    if row[1] and row[2] and row[1] in good_name_contract_code_map and row[2] == '全国均价':
                        price = row[3]
                        price = price.replace(',', '')
                        price = int(price)
                        contract_code_price[good_name_contract_code_map[row[1]]] = price
    return contract_code_price


def get_pdf_path():
    desc_dir = r'../z_pdf/new/'
    pdf_path = os.listdir(desc_dir)
    pdf_path = [os.path.join(desc_dir, pdf_path_now) for pdf_path_now in pdf_path]
    return pdf_path


def write_db(date_now, contract_code_price):
    data = {"contract_code": [], "spot_price": [], "trade_date": []}
    for contract_code, spot_price in contract_code_price.items():
        data["contract_code"].append(contract_code)
        data["spot_price"].append(spot_price)
        data["trade_date"].append(date_now)

    df = pd.DataFrame(data)
    df.to_sql("future_spot_price", engine, index=False, if_exists="append")


def move_pdf_to_old(pdf_path_now):
    fpath, fname = os.path.split(pdf_path_now)
    fpath = fpath.replace("/new", "/old")
    pdf_path_desc = os.path.join(fpath, fname)

    shutil.move(pdf_path_now, pdf_path_desc)


def main():
    pdf_path = get_pdf_path()
    for pdf_path_now in pdf_path:
        date_now = datetime.datetime.strptime(pdf_path_now[-12:-4], '%Y%m%d')
        contract_code_price = get_spot_price(pdf_path_now)
        write_db(date_now, contract_code_price)
        move_pdf_to_old(pdf_path_now)
        print(contract_code_price)


if __name__ == '__main__':
    main()
