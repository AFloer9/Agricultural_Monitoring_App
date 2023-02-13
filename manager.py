import subprocess
import json
import requests
import csv
#with open('weatherData.txt', 'w') as file:
#    subprocess.run(['scrapy','crawl', 'weather','-s','LOG_ENABLED=False'], stdout=file)
#data  = subprocess.run('curl -X GET "https://api.weather.gov/gridpoints/PQR/122,44/forecast?units=us" -H  "accept: application/geo+json"', text=True, shell=True)#capture_output=True, shell=True)

data  = requests.get("https://api.weather.gov/gridpoints/PQR/122,44/forecast?units=us")
t = json.loads(data.text)

def dayData(day):
    data = []

    data.append(day["name"])
    data.append(str(day["temperature"]) + " " + day["temperatureUnit"])
    data.append(day["windSpeed"])
    data.append(day["shortForecast"])
    data.append(day["detailedForecast"])

    dewpoint = day['dewpoint']['value']
    data.append(str(dewpoint) + ' C')

    humidity = day['relativeHumidity']['value']
    data.append(str(humidity) + ' %')
    
    return data

def weekData(week):
    weekData = []
    
    for i in week:
        weekData.append(dayData(i))

    return weekData

data = t["properties"]["periods"]

#[print('\t*' ,i, "\n") for i in weekData(data)] # print week data
data = weekData(data)

def dataToFile(filename, week):

    with open(filename + '.csv', 'w') as file:
        csv_write = csv.writer(file, delimiter='\t')

        for i in week:
            #length = len(i)
            csv_write.writerow(i)
    # api


    # scrapy

    # 

dataToFile("api", data)
