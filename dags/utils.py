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
	time_stamp = str(datetime.date(datetime.now()))
	file_name = "current_cases_" + time_stamp + ".txt"
	with open(file_name, "w+") as covid_data:
		covid_data.write("Country: {0}\nTotal Cases: {1}\nActive Cases: {2}\nNew Cases: {3}\nNew Deaths: {4}\nUpdate on: {5}".format(current_cases["CountryOrRegion"], current_cases["TotalCases"], current_cases["ActiveCases"], current_cases["NewCases"], current_cases["NewDeaths"], current_cases["LastUpdated"]))


def render_template():



