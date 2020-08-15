import os
import json
from airflow import DAG
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from helper_utils import fetch_current_cases, create_email_content

# TODO: Place a config file in the same folder.
# TODO: Create empty variables in the driver function.
# TODO: Create a function in driver to read the config file.
covid_cfg = {}
config_file_path = os.path.dirname(os.path.abspath(__file__))
with open(config_file_path+"/covid_config.json", "r+") as jsoncfg:
	covid_cfg = json.load(ymlfile)
	print(covid_cfg)
	print(type(covid_cfg))
# TODO: Assign the variables with the values read from the config file.

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

with DAG("covid_cases_notifier", default_args=default_args) as dag:
	Task_I = PythonOperator(
		task_id = "fetch_cases",
		python_callable=fetch_current_cases
	)

	Task_II = PythonOperator(
		task_id = "create_email_content",
		python_callable=create_email_content,
		provide_context = True,
	)

	Task_III = EmailOperator(
		task_id="send_email",
		to=to_mail_id,
		subject="COVID-19 cases in {{country_name}} for {{ds}}",
		html_content="{{ task_instance.xcom_pull(task_ids='create_email_content', key='email_content') }}",
	)

Task_I >> Task_II >> Task_III
