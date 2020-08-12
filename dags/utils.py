import json
import os
from datetime import datetime, timedelta

import requests
import covid19cases as covid
from jinja2 import Environment, FileSystemLoader

def fetch_current_cases():
	"""
	Uses webscraping to fetch the current covid cases in Australia and writes it to a file.
	"""
	current_cases = covid.get_country_cases("Australia")
	file_name = "current_cases_" + str(datetime.date(datetime.now())) + ".txt"
	with open(file_name, "w+") as covid_data:
		covid_data.write("Country: {0}\nTotal Cases: {1}\nActive Cases: {2}\nNew Cases: {3}\nNew Deaths: {4}\nUpdated on: {5}".format(current_cases["CountryOrRegion"], current_cases["TotalCases"], current_cases["ActiveCases"], current_cases["NewCases"], current_cases["NewDeaths"], current_cases["LastUpdated"]))

def render_content(**context):
	cases_dict = {}
	input_file = "current_cases_" + str(datetime.date(datetime.now())) + ".txt"
	with open(input_file, "r+") as content:
		file_content = content.read().splitlines()
		cases_dict = {elem.split(": ")[0]: elem.split(": ")[1] for elem in file_content}

	str_content = f"""Country: {cases_dict['Country']}
	Total Cases: {cases_dict['Total Cases']}
	Active Cases: {cases_dict['Active Cases']}
	New Cases: {cases_dict['New Cases']}
	New Deaths: {cases_dict['New Deaths']}
	Updated on: {cases_dict['Updated on']}"""
	
	task_instance = context["task_instance"]
	task_instance.xcom_push(key="email_content", value=str_content)
