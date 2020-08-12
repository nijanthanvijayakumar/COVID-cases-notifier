import json
import os
from datetime import datetime, timedelta

import requests
import covid19cases as covid

def fetch_current_cases():
	"""
	Uses webscraping to fetch the current covid cases in Australia and writes it to a file.
	"""
	current_cases = covid.get_country_cases("Australia")
	file_name = "current_cases_" + str(datetime.date(datetime.now())) + ".txt"
	with open(file_name, "w+") as covid_data:
		covid_data.write("Country\t: {0}\nTotal Cases\t: {1}\nActive Cases\t: {2}\nNew Cases\t: {3}\nNew Deaths\t: {4}\nUpdate on\t: {5}".format(current_cases["CountryOrRegion"], current_cases["TotalCases"], current_cases["ActiveCases"], current_cases["NewCases"], current_cases["NewDeaths"], current_cases["LastUpdated"]))

def render_content(**context):
