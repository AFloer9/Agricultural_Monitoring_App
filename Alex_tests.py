# Author: Alexander Flores Spring 2023 Class: CS 320
import unittest
from api.geo_open_weather_api import gen_city_coordinates, gen_zip_coordinates, get_geo_data
from api.open_weather_api import run_open_weather_api, gen_forecast_url
from api.noaa_api import gen_url, run_noaa_api
from api.tools import gen_attribute
from api.weather_gov import dayData, weekData, dataToFile, run_weather_gov
from os import path, remove
#import api.test

try:
    from api.secret import SK, Token, ZIP
except:
    raise Exception("Tests required SK (token for open weather api), Token (token for noaa api), and ZIP in file api.secret")

class TestOpenWeather(unittest.TestCase):
    def test_gen_attributes(self):
        # acceptance test
        a = gen_attribute('test', 'pass')
        self.assertEqual(a, '&test=pass')
        
        a = gen_attribute('teest', 'fail')
        self.assertNotEqual(a, '&test=fail')
        
        a = gen_attribute('test', 'faail')
        self.assertNotEqual(a, '&test=fail')


    def test_get_geo_data(self):
# White-box test: condition coverage
# testing function below
#        def get_geo_data(data_dict):
#            city = ''
#            if 'name' in data_dict:
#                city = data_dict['name']
#            country = ''
#            if 'country' in data_dict:
#                country = data_dict['country']
#            lat = ''
#            if 'lat' in data_dict:
#                lat = str(data_dict['lat'])
#            lon = ''
#            if 'lon' in data_dict:
#                lon = str(data_dict['lon'])
# 
#            if not lat or not lon:
#                return None
# 
#            return (city, country, lat, lon)

        data = {'name':'Vancouver', 'country':'US', 'lat':'45', 'lon':'-122'}
        a = get_geo_data(data)
        self.assertEqual(a, ('Vancouver', 'US', '45', '-122'))
        
        too_much_data = {'name':'Vancouver', 'country':'US', 'lat':'45', 'lon':'-122', 'nothing': 'Error'}
        a = get_geo_data(too_much_data)
        self.assertEqual(a, ('Vancouver', 'US', '45', '-122'))
        
        no_name_data = {'country':'US', 'lat':'45', 'lon':'-122'}
        a = get_geo_data(no_name_data)
        self.assertEqual(a, ('', 'US', '45', '-122'))
        no_country_data = {'name':'Vancouver', 'lat':'45', 'lon':'-122'}
        a = get_geo_data(no_country_data)
        self.assertEqual(a, ('Vancouver', '', '45', '-122'))
        no_location_data = {'lat':'45', 'lon':'-122'}
        a = get_geo_data(no_location_data)
        self.assertEqual(a, ('', '', '45', '-122'))
        
        no_latitude_data = {'name':'Vancouver', 'country':'US', 'lon':'-122'}
        a = get_geo_data(no_latitude_data)
        self.assertIsNone(a)
        no_longitude_data = {'name':'Vancouver', 'country':'US', 'lat':'45', }
        a = get_geo_data(no_longitude_data)
        self.assertIsNone(a)
        no_coordinate_data = {'name':'Vancouver', 'country':'US'}
        a = get_geo_data(no_coordinate_data)
        self.assertIsNone(a)

#    @unittest.skip('skip bc it will waste api call')
    def test_gen_city_coordinates(self):
        # acceptance test
        # dont need to check incorrect key because it will error out

        a =  gen_city_coordinates('Vancouver', 'Washington', 'US', SK)
        self.assertEqual(a, ('Vancouver', 'US', '45.6306954', '-122.6744557'))
        
        a =  gen_city_coordinates('Vancouver', 'bad data', 'US', SK)
        self.assertIsNone(a)
    
#    @unittest.skip('skip bc it will waste api call')
    def test_gen_zip_coordinates(self):
        # acceptance test
        a = gen_zip_coordinates(ZIP, SK)
        self.assertEqual(a, ('Vancouver', 'US', '45.6418', '-122.6251'))
        a = gen_zip_coordinates(ZIP, SK, 'US')
        self.assertEqual(a, ('Vancouver', 'US', '45.6418', '-122.6251'))

        # bad data
        a = gen_zip_coordinates(ZIP + 'A', SK)
        self.assertIsNone(a)

    
#    @unittest.skip('skip bc it will waste api call')
    def test_gen_forecast_url(self):
        # acceptance test
        data = gen_city_coordinates('Vancouver', 'Washington', 'US', SK)
        lat = data[2]
        lon = data[3]

        a = gen_forecast_url(SK, lat, lon)
        url = f'https://api.openweathermap.org/data/2.5/forecast?&lat={lat}&lon={lon}&units=imperial&lang=en' + gen_attribute('appid', SK)
        self.assertEqual(a, url)
    
#    @unittest.skip('skip bc it will waste api call')
    def test_run_open_weather_api(self):
        # Integration test: big bang
        # using the geo_open_weather module with the open_weather_api module.
        # with the first module i get the latitude and longitude of a location.
        # with the second module I use the lat and lon to find the 5 day forecast
        # (40 different 3-hour intervals) 
        data = gen_city_coordinates('Vancouver', 'Washington', 'US', SK)
        lat = data[2]
        lon = data[3]

        self.assertEqual(len(run_open_weather_api(SK, lat, lon)), 40)

        bad_lat = '-91'
        bad_lon = '-181'

        self.assertIsNone(run_open_weather_api(SK, bad_lat, lon))
        self.assertIsNone(run_open_weather_api(SK, lat, bad_lon))

        bad_SK = '5'
        self.assertIsNone(run_open_weather_api(bad_SK, lat, lon))


class TestNOAA(unittest.TestCase):
#    @unittest.skip('skip bc it will waste api call')
    def test_gen_url(self):
        # acceptance test
        a = gen_url('2023-01-01', '2023-02-01', 'TMAX', ZIP)
        url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/data?&limit=1000&locationid=ZIP:' + \
                f'{ZIP}&datasetid=GHCND&datatypeid=TMAX&startdate=2023-01-01' + \
                '&enddate=2023-02-01&includemetadata=false&units=metric'
        self.assertEqual(a, url)

#    @unittest.skip('skip bc it will waste api call')
    def test_run_noaa_api(self):
        # acceptance test
        self.assertIsNot(len(run_noaa_api(Token, '2023-01-01', '2023-02-01', 'TMAX', ZIP)), 0)
        
        self.assertIsNone(run_noaa_api(Token, '2023-01-01', '2023-02-01', 'dsds', ZIP))
        self.assertIsNone(run_noaa_api(Token, '2023-01-01', '2023-02-01', 'TMAX', ZIP + '0'))
        self.assertIsNone(run_noaa_api(Token, '2099-01-01', '2099-02-01', 'TMAX', ZIP))
        
        self.assertIsNone(run_noaa_api('5', '2023-01-01', '2023-02-01', 'TMAX', ZIP))
        

class TestWeatherGov(unittest.TestCase):
    def setUp(self):
        self.data = {'name':'Monday', 'temperature':'70', 'temperatureUnit':'F', \
                'windSpeed':'70', 'shortForecast':'Something', 'detailedForecast':'Something else',\
                'dewpoint':{'value':'7'}, 'relativeHumidity':{'value':'7'}}
        self.val = ['Monday', '70 F', '70', 'Something', 'Something else', '7 C', '7 %']
        

    def test_day_data(self):
        # acceptance test

        a = dayData(self.data)

        self.assertEqual(a, self.val)


    def test_week_data(self):
        # acceptance test
        data = [self.data for i in range(40)]
        val = [self.val for i in range(40)]

        a = weekData(data)

        self.assertEqual(a, val)


    def test_data_to_file(self):
        # acceptance test
        val = [self.val for i in range(40)]
        non_existent_filename = 'dasdasdsadswqeqgnqqwmeoqwmwqoemqoei'

        dataToFile(non_existent_filename, val)

        f = open(non_existent_filename + '.csv', 'r')
        
        a = [line.split('\t') for line in f]

        f.close()
        remove(non_existent_filename + '.csv')
       
        for row in a:
            row[-1] = row[-1][0:3]
        
        self.assertEqual(a, val)


    def test_run_weather_gov(self):
        # acceptance test
        lat = 45
        lon = 122
        filename = 'weather_gov_data.csv'
        
        run_weather_gov(lat, lon)
        
        a = path.isfile(filename)
        
        remove(filename)
        
        self.assertTrue(a)


class TestWebcrawler(unittest.TestCase):
    def test_nothing(self):
        pass


if __name__ == '__main__':
    unittest.main()


