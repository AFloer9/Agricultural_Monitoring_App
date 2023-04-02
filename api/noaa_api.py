import json
import requests
from datetime import datetime
from time import sleep
from api.tools import gen_attribute

def gen_url(start_date, end_date, data_type, zip_code):
    base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data?"
    metadata = gen_attribute('includemetadata', 'false') + gen_attribute('units', 'metric')
    
    location = gen_attribute('locationid', f'ZIP:{zip_code}')
    dataset = gen_attribute('datasetid', 'GHCND')
    datatype = gen_attribute('datatypeid', data_type)
    startdate =  gen_attribute('startdate', start_date)
    enddate = gen_attribute('enddate', end_date)
    limit = gen_attribute('limit', '1000')
    
    return base_url + limit + location + dataset + datatype + startdate + enddate + metadata


def run_noaa_api(token, start_date, end_date, data_type, zip_code):
    url = gen_url(start_date, end_date, data_type, zip_code)
    
    r = requests.get(url, headers={'token':token})
    data = json.loads(r.text)
    
    if len(data) == 0: # params not within range of api
        return None
    if 'status' in data: # token error
        return None
    
    return data['results']
    
