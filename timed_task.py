import datetime
import logging
import threading
import time
from logging import handlers

import schedule

from source.trade_data_get import security_point_data, security_daily_basic_data
from source.trade_result_send import update_tactics_success_num, update_tactics_success_rate, update_not_sent_result_status
from source.trade_result_send.send_result import send_bs_result

logger = logging.getLogger('/home/stock/app/security_data_store/timed_task')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

rf = handlers.RotatingFileHandler('./timed_task.log', encoding='UTF-8', maxBytes=124, backupCount=0)
rf.setLevel(logging.INFO)
rf.setFormatter(formatter)

logger.addHandler(rf)


def job1():
    date_now = datetime.datetime.now()
    date_now = datetime.datetime(date_now.year, date_now.month, date_now.day)

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

    try:
        logger.info('starting update_tactics_success_num')
        update_tactics_success_num.update_tactics_success_num(date_now)
    except Exception as e:
        logger.error('error update_tactics_success_num, {0}'.format(str(e)))
    logger.info('finished update_tactics_success_num')

    try:
        logger.info('starting update_tactics_success_rate')
        update_tactics_success_rate.update_tactics_success_rate(date_now)
    except Exception as e:
        logger.error('error update_tactics_success_rate, {0}'.format(str(e)))
    logger.info('finished update_tactics_success_rate')


def job1_task():
    threading.Thread(target=job1).start()


def job2():
    try:
        logger.info('starting update_not_sent_result_status')
        update_not_sent_result_status.update_not_sent_result_status()
    except Exception as e:
        logger.error('error update_not_sent_result_status, {0}'.format(str(e)))
    logger.info('finished update_not_sent_result_status')

    try:
        logger.info('starting send_bs_result')
        send_bs_result()
    except Exception as e:
        logger.error('error send_bs_result, {0}'.format(str(e)))
    logger.info('finished send_bs_result')


def job3():
    """现在指数相关的所有指标都不太好使, 暂时都不加定时任务"""
    pass


def run():
    schedule.every().day.at("20:00").do(job1_task)
    # schedule.every(5).minutes.do(job2)
    schedule.every().day.at("5:30").do(job2)
    schedule.every().day.at("1:30").do(job3)


if __name__ == "__main__":
    run()
    while True:
        schedule.run_pending()
        time.sleep(1)
