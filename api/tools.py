# Author: Alexander Flores Spring 2023 Class: CS 320
from datetime import datetime

def gen_attribute(variable, data):
    return f"&{variable}={data}"

def unix_to_datetime(t):
    return datetime.fromtimestamp(t)#.date() # utcfromtimestamp(t)

def datetime_to_unix(t):
    return t.timestamp()

#o = unix_to_datetime(1679378400)
#print(o)
#o = o.timestamp()#datetime_to_unix(0)
#print(o)


