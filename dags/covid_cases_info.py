from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from utils import fetch_current_cases

default_args = {
    "owner": "me",
    "depends_on_past": False,
    "start_date": datetime(2019, 10, 9),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
    "schedule_interval": "@daily",
}

with DAG("covid_cases_notifier", default_args=default_args) as dag:
	Task_I = PythonOperator(
		task_id = "fetch_cases", python_callable=fetch_current_cases
	)

Task_I
