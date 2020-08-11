from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    "owner": "me",
    "depends_on_past": False,
    "start_date": datetime(2019, 10, 9),
    # "email": ["my_email@mail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
    "schedule_interval": "@daily",
}

with DAG("google_news", default_args=default_args) as dag:
	Task_I = PythonOperator(
		task_id = "fetch_latest_news"
	)

	Task_II = PythonOperator(
		task_id = "write_news_to_s3"
	)

Task_I >> Task_II