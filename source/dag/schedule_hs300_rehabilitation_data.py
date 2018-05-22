import sys

# sys.path.append('/home/stock/app')
sys.path.append('/home/stock/app/security_data_store')

from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG
import datetime
from source.trade_data_get import hs300_rehabilitation_data

args = {
    "owner": "flydedog",
    "start_date": datetime.datetime(2018, 5, 19),
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
    "email": ["flydedog@163.com"],
    "email_on_failure": False
}

dag = DAG(
    dag_id="hs300_rehabilitation_data",
    default_args=args,
    schedule_interval="0 5 * * *"
)

get_hs300_rehabilitation_data = PythonOperator(
    task_id="get_hs300_rehabilitation_data",
    python_callable=hs300_rehabilitation_data.start,
    op_kwargs={},
    dag=dag
)
