from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from utils import fetch_current_cases, render_content

default_args = {
    "owner": "me",
    "depends_on_past": False,
    "start_date": datetime(2020, 8, 12),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=15),
    "schedule_interval": "@daily",
}

with DAG("covid_cases_notifier", default_args=default_args) as dag:
	Task_I = PythonOperator(
		task_id = "fetch_cases",
		python_callable=fetch_current_cases
	)

	Task_II = PythonOperator(
		task_id = "render_content",
		python_callable=render_content,
		provide_context = True,
	)

	Task_III = EmailOperator(
		task_id="send_email",
		to="niju.vijayakumar@accenture.com",
		subject="COVID-19 Cases in Australia for {{ds}}",
		html_content="{{ task_instance.xcom_pull(task_ids='render_content', key='email_content') }}",
	)

Task_I >> Task_II >> Task_III
