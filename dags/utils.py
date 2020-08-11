import json
import os
from datetime import datetime, timedelta

import requests
from airflow.hooks.S3_hook import S3Hook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable

from jinja2 import Environment, FileSystemLoader

import covid19cases as covid

def fetch_current_cases():
	current_cases = covid.get_country_cases("Australia")
	country = current_cases["CountryOrRegion"]
	total_cases = current_cases["TotalCases"]
	active_cases = current_cases["ActiveCases"]
	new_cases = current_cases["NewCases"]
	new_deaths = current_cases["NewDeaths"]
	updated_on = current_cases["LastUpdated"]
	time_stamp = datetime.date(datetime.now())
	file_name = "current_cases_" + time_stamp + ".txt"
	with open(file_name, "w+") as covid_data:
		covid_data.write("""
			Country: {0}
			Total Cases: {1}
			Active Cases: {2}
			New Cases: {3}
			New Deaths: {4}
			Update on: {5}
			""".format(country, total_cases, active_cases, new_cases, new_deaths, updated_on))



