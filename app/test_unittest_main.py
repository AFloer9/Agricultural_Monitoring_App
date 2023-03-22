#testing framework = pytest
import unittest #testing library
from unittest.mock import patch #allows mocking of object during test
import requests
from pydanticmodels import Seed 
#import main #import file to test
from main import app #import app object
from fastapi import HTTPException, status 

class TestMain(unittest.TestCase): 
    #tests cases inherit from TestCase
    
    def setUp(self):    #pre-assign variable values for tests--SQLAlchemy models
        self.seed_1 = Seed(id= 10, seed_type='marigold', coll_loc='backyard', num_coll=20)
        self.seed_2 = Seed(id= 2, seed_type='daisy', coll_loc='field', num_coll=20)
    
#test format:    
#def test_name(self):
    #self.assertLogic(condition)
    #Logic = True, False, Equal, NotEqual, ETC.

  #  def test_http_ret(self):
   #     self.assertTrue()
                
        
    def test_get_main_page(self):   #method in class
        #response = app.get('/') 
        #self.assertEqual(response, 200)
        #above 2 lines same as: 
        #self.assertEqual(app.get('http://127.0.0.1'), 200) #one-liner
        #self.assertEqual(app.get('/'), 200) #one-liner
        self.assertEqual(app.get('/'), {"Welcome to ": "the Agricultural Monitoring Project"}) #one-liner
        
    def test_get_oneseed(self):   #method in class
        with patch('main.get_seed') as mock_get:
            mock_get.return_value.seed_type = 'marigold'
            test_seed = self.seed_1
            mock_get.assert_called_with('http://127.0.0.1/seedvault/1')
            self.assertEqual(test_seed, 'marigold')
            
            
        
if __name__ == '__main__':  #run code within conditional
    unittest.main()        
        
        
#possible tests:
#what is returned after http request (http code)
#

#For Assignment: 12 automated tests

#at least one test of each type (although you will need more than 1 acceptance test)

#BLACK BOX acceptance test--mark as "acceptance test" in the comments. 
#acceptance tests must thoroughly test some requirement or feature from your cool-cam.

#WHITE BOX tests--write what kind of coverage they provide and 
# include a copy of the function/procedure/method being tested as a comment. 
# If a single test does not yield complete coverage, 
# you can state "along with [other test], achieves X coverage."

#INTEGRATION tests--must exercise two units at once. Both may come from your cool cam 
# or from team-mates cool cams, as long as you write the tests yourself. 
# In the comments, write which units are being tested and what your approach is 
# (bottom-up, top-down, big-bang, etc.). 
# Remember, a unit is typically a class. 
