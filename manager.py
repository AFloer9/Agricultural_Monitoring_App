import subprocess
import json
import requests
#with open('weatherData.txt', 'w') as file:
#    subprocess.run(['scrapy','crawl', 'weather','-s','LOG_ENABLED=False'], stdout=file)
#data  = subprocess.run('curl -X GET "https://api.weather.gov/gridpoints/PQR/122,44/forecast?units=us" -H  "accept: application/geo+json"', text=True, shell=True)#capture_output=True, shell=True)
data  = requests.get("https://api.weather.gov/gridpoints/PQR/122,44/forecast?units=us")
t = json.loads(data.text)

print(type(t))
print(t.keys())
print(t["properties"].keys())
print(len(t["properties"]["periods"]))
print(type(t["properties"]["periods"][0]))
print(data.text)
#print(data)
#data = json.load(data)
