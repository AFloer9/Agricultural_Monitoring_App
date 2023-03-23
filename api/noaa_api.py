import json
import requests
from datetime import datetime
from time import sleep


def gen_url(start_date, end_date, data_type):
    base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data?"
    metadata = gen_attribute('includemetadata', 'false') + gen_attribute('units', 'metric')
    
    location = gen_attribute('locationid', 'ZIP:98661')
    dataset = gen_attribute('datasetid', 'GHCND')
    datatype = gen_attribute('datatypeid', data_type)
    startdate =  gen_attribute('startdate', start_date)
    enddate = gen_attribute('enddate', end_date)
    limit = gen_attribute('limit', '1000')
    
    return base_url + limit + location + dataset + datatype + startdate + enddate + metadata


def run_noaa_api(token, start_date, end_date, data_type):
    url = gen_url(start_date, end_date, data_type)
    
    r = requests.get(url, headers={'token':token})
    data = json.loads(r.text)
    
    if len(data) == 0:
        return 0
    
    result = data['results']
    
    i = len(result)
    print(f"Total {data_type}:{i}")
    return i
    
