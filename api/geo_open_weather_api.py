from json import loads
from requests import get
from api.tools import gen_attribute


def get_geo_data(data_dict):
    city = ''
    if 'name' in data_dict:
        city = data_dict['name']
    country = ''
    if 'country' in data_dict:
        country = data_dict['country']
    lat = ''
    if 'lat' in data_dict:
        lat = data_dict['lat']
    lon = ''
    if 'lon' in data_dict:
        lon = data_dict['lon']

    if not lat or not lon:
        return None

    return (city, country, lat, lon)


def gen_city_coordinates(city, state, country, key):
    # county needs to follow ISO 3166 code
    
    base_url = 'http://api.openweathermap.org/geo/1.0/direct?'
    location = city + ',' + state + ',' + str(country)
    city_name = gen_attribute('q', location)
    key = gen_attribute('appid', key)
    
    request = get(base_url + city_name + key)
    data = loads(request.text)
    
    if len(data) == 0:
        return None

    return get_geo_data(data[0])


def gen_zip_coordinates(zip_code, key, country=''):
    # county needs to follow ISO 3166 code (Alpha-Code 2)
    
    base_url = 'http://api.openweathermap.org/geo/1.0/zip?'
    location = (zip_code + ',' + str(country)) if '' != country else zip_code
    
    zip_param = gen_attribute('zip', location)
    key_param = gen_attribute('appid', key)
    
    request = get(base_url + zip_param + key_param)
    data = loads(request.text)
    
    if len(data) == 0 or 'cod' in data:
        return None

    return get_geo_data(data)


