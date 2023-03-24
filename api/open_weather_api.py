from json import loads
from requests import get
from api.tools import gen_attribute
from api.geo_open_weather_api import gen_city_coordinates, gen_zip_coordinates


def gen_forecast_url(key, lat, lon):
    base_url = 'https://api.openweathermap.org/data/2.5/forecast?'
    language = gen_attribute('lang', 'en')
    units = gen_attribute('units', 'imperial')

    key = gen_attribute('appid', key)
    location = gen_attribute('lat', lat) + gen_attribute('lon', lon)
    
    return base_url + location + units + language + key


def run_open_weather_api(key, lat, lon):
    if lat < -90 or lat > 90:
        return None
    if lon < -180 or lon > 180:
        return None

    url = gen_forecast_url(key, lat, lon)

    r = get(url)
    data = loads(r.text)
    
    if data['cod'] != '200':
        return None
    
    i = 0
    for col in data['list']:
        i += 1
        print(col)
    print(f"Total: {i}")


