# Author: Alexander Flores Spring 2023 Class: CS 320
from pathlib import Path
import scrapy

class WeatherData(scrapy.Spider):
    name = "weather"
    start_urls = [
            'https://forecast.weather.gov/MapClick.php?lat=45.632480000000044&lon=-122.7155999999994'
            ]
    allowed_domains = ['forecast.weather.gov']
    
    def removeNewline(self, array):
        return [i.replace('\n', '') for i in array]

    def parse(self, response):
        
        currentWeatherData = 'div.panel-body '
        currentWeather = response.css(currentWeatherData + 'div.pull-left p::text').getall()
        currentData = response.css(currentWeatherData + 'div.pull-left table tr b::text').getall()
        data = response.css(currentWeatherData + 'div.pull-left table td::text').getall()
        
        print(self.removeNewline(currentWeather))
        print(self.removeNewline(currentData))
        print(self.removeNewline(data))
        
        sevenDayForecast = 'ul.list-unstyled li.forecast-tombstone '
        weekName = response.css( sevenDayForecast + 'p.period-name::text' ).getall()
        weekWeather = response.css( sevenDayForecast + 'p.temp::text' ).getall()
        
        print(self.removeNewline(weekName))
        print(self.removeNewline(weekWeather))
