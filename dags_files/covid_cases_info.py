import os
import json
from airflow import DAG
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from helper_utils import fetch_current_cases, create_email_content

# Read the JSON config file to get dynamic input values to DAG
covid_cfg = {}
config_file_path = os.path.dirname(os.path.abspath(__file__))
with open(config_file_path+"/covid_config.json", "r+") as jsoncfg:
	covid_cfg = json.load(jsoncfg)
	
# Form the arguments to be passed to DAG
default_args = {
    "owner": "me",
    "depends_on_past": False,
    "start_date": datetime(2020, 8, 13),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=15),
    "schedule_interval": "@daily",
    "to_mail_id": covid_cfg["to_email"],
    "country_name": covid_cfg["country"]
}

# Define the DAG and tasks within the DAG.
with DAG("covid_cases_notifier", default_args=default_args) as dag:
	Task_I = PythonOperator(
		task_id = "fetch_cases",
		python_callable = fetch_current_cases,
		op_args = [default_args["country_name"]]
	)

	Task_II = PythonOperator(
		task_id = "create_email_content",
		python_callable = create_email_content,
		provide_context = True,
	)

	Task_III = EmailOperator(
		task_id="send_email",
		to=default_args["to_mail_id"],
		subject="COVID-19 cases in {0} for {{ds}}".format(default_args["country_name"]),
		html_content="{{ task_instance.xcom_pull(task_ids='create_email_content', key='email_content') }}",
	)

# Define the order of execution of the DAG
Task_I >> Task_II >> Task_III
