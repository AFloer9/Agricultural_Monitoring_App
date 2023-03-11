
import unittest #import testing framework
#import main #import file to test

class TestMain(unittest.TestCase): 
    #tests cases inherit from TestCase
    
#test format:    
#def test_name(self):
    #self.assertLogic(condition)
    #Logic = True, False, Equal, Raises (exception raised)

    def test_http_ret(self):
        self.assertTrue()
        
        
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
