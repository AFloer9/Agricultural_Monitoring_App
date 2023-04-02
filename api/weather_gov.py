import requests
import json
import csv


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


def run_weather_gov(lat, lon):
    # return none if lat or lon less than 0
    url = f"https://api.weather.gov/gridpoints/PQR/{lon},{lat}/forecast?units=us"
    
    req  = requests.get(url)
    dic = json.loads(req.text)
    
    data = dic["properties"]["periods"] # get weather data

    #[print('\t*' ,i, "\n") for i in weekData(data)] # print week data
    data = weekData(data)
    dataToFile("weather_gov_data", data)

#run_weather_gov(-45, 122)
