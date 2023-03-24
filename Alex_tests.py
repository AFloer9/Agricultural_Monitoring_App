import unittest
from api.geo_open_weather_api import gen_city_coordinates, gen_zip_coordinates, get_geo_data
from api.open_weather_api import run_open_weather_api, gen_forecast_url
from api.noaa_api import gen_url, run_noaa_api
from api.tools import gen_attribute
try:
    from api.secret import SK, Token
except:
    raise Exception("Tests required SK (token for open weather api) and Token (token for noaa api) in file api.secret")

class TestOpenWeather(unittest.TestCase):
    def test_gen_attributes(self):
        a = gen_attribute('test', 'pass')
        self.assertEqual(a, '&test=pass')
        
        a = gen_attribute('teest', 'fail')
        self.assertNotEqual(a, '&test=fail')
        
        a = gen_attribute('test', 'faail')
        self.assertNotEqual(a, '&test=fail')


    def test_get_geo_data(self):
        enough_data = {'name':'Vancouver', 'country':'Washington', 'lat':'45.6418', 'lon':'-122.6251'}
        a = get_geo_data(enough_data)
        
        too_much_data = {'name':'Vancouver', 'country':'Washington', 'lat':'45.6418', 'lon':'-122.6251', 'nothing': 'Error'}
        a = get_geo_data(too_much_data)
        self.assertEqual(a, ('Vancouver', 'Washington', '45.6418', '-122.6251'))
        
        not_enough_data = {'country':'Washington', 'lat':'45.6418', 'lon':'-122.6251'}
        a = get_geo_data(not_enough_data)
        self.assertEqual(a, ('', 'Washington', '45.6418', '-122.6251'))
        not_enough_data = {'name':'Vancouver', 'lat':'45.6418', 'lon':'-122.6251'}
        a = get_geo_data(not_enough_data)
        self.assertEqual(a, ('Vancouver', '', '45.6418', '-122.6251'))
        not_enough_data = {'name':'Vancouver', 'country':'Washington', 'lon':'-122.6251'}
        a = get_geo_data(not_enough_data)
        self.assertIsNone(a)
        not_enough_data = {'name':'Vancouver', 'country':'Washington', 'lat':'45.6418', }
        a = get_geo_data(not_enough_data)
        self.assertIsNone(a)
        not_enough_data = {'name':'Vancouver', 'country':'Washington'}
        a = get_geo_data(not_enough_data)
        self.assertIsNone(a)
        not_enough_data = {'lat':'45.6418', 'lon':'-122.6251'}
        a = get_geo_data(not_enough_data)
        self.assertEqual(a, ('', '', '45.6418', '-122.6251'))



#class Test(unittest.TestCase):
#    pass

#class Test(unittest.TestCase):
#    pass

#class Test(unittest.TestCase):
#    pass

#class Test(unittest.TestCase):
#    pass

#class Test(unittest.TestCase):
#    pass

#class Test(unittest.TestCase):
#    pass

#class Test(unittest.TestCase):
#    pass

#class Test(unittest.TestCase):
#    pass

#class Test(unittest.TestCase):
#    pass

#class Test(unittest.TestCase):
#    pass

#class Test(unittest.TestCase):
#    pass

if __name__ == '__main__':
    unittest.main()

