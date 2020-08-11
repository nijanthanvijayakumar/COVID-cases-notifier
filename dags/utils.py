import json
import os
from datetime import datetime, timedelta

import requests
from airflow.hooks.S3_hook import S3Hook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable

from jinja2 import Environment, FileSystemLoader