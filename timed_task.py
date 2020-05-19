import datetime
import logging
import threading
import time
from logging import handlers

import schedule

from index_data_get import index_point_data
from market_data_get import stock_holder_number_data, future_main_holding_data, future_main_code_data, future_basic_info_data
from trade_data_get import security_point_data, security_daily_basic_data, future_daily_point_data

logger = logging.getLogger('/home/stock/app/security_data_store/timed_task')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

rf = handlers.RotatingFileHandler('./timed_task.log', encoding='UTF-8', maxBytes=124, backupCount=0)
rf.setLevel(logging.INFO)
rf.setFormatter(formatter)

logger.addHandler(rf)


def security_number_job():
    try:
        logger.info('starting stock_holder_number_data')
        stock_holder_number_data.start()
    except Exception as e:
        logger.error('error stock_holder_number_data, {0}'.format(str(e)))
    logger.info('finished stock_holder_number_data')


def stock_security_number_job_task():
    threading.Thread(target=security_number_job).start()


def future_daily_point_job():
    try:
        logger.info('starting future_daily_point_data')
        future_daily_point_data.start()
    except Exception as e:
        logger.error('error future_daily_point_data, {0}'.format(str(e)))
    logger.info('finished future_daily_point_data')

    try:
        logger.info('starting future_main_holding_data')
        future_main_holding_data.start()
    except Exception as e:
        logger.error('error future_main_holding_data, {0}'.format(str(e)))
    logger.info('finished future_main_holding_data')


def future_daily_point_task_job():
    threading.Thread(target=future_daily_point_job).start()


def stock_daily_point_job():
    try:
        logger.info('starting security_point_data')
        security_point_data.start()
    except Exception as e:
        logger.error('error security_point_data, {0}'.format(str(e)))
    logger.info('finished security_point_data')

    try:
        logger.info('starting security_daily_basic_data')
        security_daily_basic_data.start()
    except Exception as e:
        logger.error('error security_daily_basic_data, {0}'.format(str(e)))
    logger.info('finished security_daily_basic_data')


def stock_daily_point_task_job():
    threading.Thread(target=stock_daily_point_job).start()


def future_market_data_job():
    try:
        logger.info('starting future_basic_info_data')
        future_basic_info_data.start()
    except Exception as e:
        logger.error('error future_basic_info_data, {0}'.format(str(e)))
    logger.info('finished future_basic_info_data')

    try:
        logger.info('starting future_main_code_data')
        future_main_code_data.start()
    except Exception as e:
        logger.error('error future_main_code_data, {0}'.format(str(e)))
    logger.info('finished future_main_code_data')


def stock_index_job():
    """现在指数相关的所有指标都不太好使, 暂时都不加定时任务"""
    try:
        logger.info('starting index_point_data')
        index_point_data.start()
    except Exception as e:
        logger.error('error index_point_data, {0}'.format(str(e)))
    logger.info('finished index_point_data')


def run():
    date_now = datetime.datetime.now()
    logger.info('starting security_data_store, date={0}'.format(date_now))

    schedule.every().day.at("19:00").do(stock_index_job)
    schedule.every().day.at("18:30").do(stock_security_number_job_task)
    schedule.every().day.at("19:20").do(stock_daily_point_task_job)

    schedule.every().day.at("21:05").do(future_market_data_job)
    schedule.every().day.at("21:10").do(future_daily_point_task_job)

    # schedule.every(5).minutes.do(job2)

    logger.info('finished security_data_store, date={0}'.format(date_now))


if __name__ == "__main__":
    run()
    while True:
        schedule.run_pending()
        time.sleep(1)
