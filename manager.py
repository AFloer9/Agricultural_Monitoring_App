import subprocess
import json
import requests
import csv
import os

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


def dataToFile(filename, week):

    with open(filename + '.csv', 'w') as file:
        csv_write = csv.writer(file, delimiter='\t')

        for i in week:
            csv_write.writerow(i)

def weatherToCSV(filename):
    with open(filename +'.txt', 'r') as file:
        with open(filename + '.csv', 'w') as f:
            csv_write = csv.writer(f, delimiter='\t')
            for line in file:
                csv_write.writerow(line[1:-2].replace("'", '').split(','))


def manager():
    # run each program
    
    # api
    req  = requests.get("https://api.weather.gov/gridpoints/PQR/122,44/forecast?units=us")
    dic = json.loads(req.text)
    
    data = dic["properties"]["periods"] # get weather data
    
    #[print('\t*' ,i, "\n") for i in weekData(data)] # print week data
    data = weekData(data)
    dataToFile("api", data)

    # scrapy
    filename = 'weatherData'
    with open(filename + '.txt', 'w') as file:
        subprocess.run(['scrapy','crawl', 'weather','-s','LOG_ENABLED=False'], stdout=file)
        weatherToCSV(filename)

        os.remove(filename + '.txt')
    
    # arduino


manager()

