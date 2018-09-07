import threading
import time

import schedule

from source.trade_data_get import hs300_rehabilitation_data


def job1():
    hs300_rehabilitation_data.start()


def job1_task():
    threading.Thread(target=job1).start()


def run():
    schedule.every().day.at("5:00").do(job1_task)


if __name__ == "__main__":
    run()
    while True:
        schedule.run_pending()
        time.sleep(1)
