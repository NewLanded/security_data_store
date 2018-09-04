import datetime

from airflow.models import DAG
from airflow.operators.email_operator import EmailOperator

args = {
    "owner": "flydedog",
    "start_date": datetime.datetime(2018, 5, 24),
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
    "email": ["flydedog@163.com"],
    "email_on_failure": True
}

dag = DAG(
    dag_id="work_check",
    default_args=args,
    # schedule_interval="40 9 * * *"
    schedule_interval="40 9 * * 1-5"
)

email_task = EmailOperator(
    to='flydedog@163.com',
    task_id='email_task',
    subject='work_check_mention',
    params={},
    html_content="打卡. 考勤",
    dag=dag)
