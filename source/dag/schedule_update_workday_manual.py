import datetime

from airflow.models import DAG
from airflow.operators.email_operator import EmailOperator

args = {
    "owner": "flydedog",
    "start_date": datetime.datetime(2018, 5, 26),
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
    "email": ["flydedog@163.com"],
    "email_on_failure": True
}

dag = DAG(
    dag_id="update_workday_manual",
    default_args=args,
    # schedule_interval="40 9 * * *"
    schedule_interval="0 12 29,30,31 12 *"
)

email_task = EmailOperator(
    to='flydedog@163.com',
    task_id='email_task',
    subject='update_workday_manual',
    params={},
    html_content="更新表sec_date_info中的节假日数据",
    dag=dag)
