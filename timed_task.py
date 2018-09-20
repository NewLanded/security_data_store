import logging
import threading
import time
from logging import handlers

import schedule

from source.trade_data_get import hs300_rehabilitation_data
from source.trade_result_send.send_result import send_bs_result

logger = logging.getLogger('/home/stock/app/security_data_store/timed_task')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

rf = handlers.RotatingFileHandler('./timed_task.log', encoding='UTF-8', maxBytes=124, backupCount=0)
rf.setLevel(logging.INFO)
rf.setFormatter(formatter)

logger.addHandler(rf)


def job1():
    logger.info('starting hs300_rehabilitation_data')
    try:
        hs300_rehabilitation_data.start()
    except Exception as e:
        logger.error('error hs300_rehabilitation_data, {0}'.format(str(e)))
    logger.info('finished hs300_rehabilitation_data')


def job1_task():
    threading.Thread(target=job1).start()


def job2():
    send_bs_result()


def run():
    schedule.every().day.at("5:00").do(job1_task)
    schedule.every(5).minutes.do(job2)


if __name__ == "__main__":
    run()
    while True:
        schedule.run_pending()
        time.sleep(1)
