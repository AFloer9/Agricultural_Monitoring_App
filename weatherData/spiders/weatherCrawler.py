from pathlib import Path

import scrapy

class WeatherData(scrapy.Spider):
    name = "weather"
    start_urls = [
            'https://forecast.weather.gov/MapClick.php?lat=45.63854500000008&lon=-122.64183499999996'
            ]
    allowed_domains = ['forecast.weather.gov']

    def parse(self, response):
        filename = 'weather.html'

        currentWeatherData = 'div.panel-body '
        currentWeather = response.css(currentWeatherData + 'div.pull-left p::text').getall()
        #print(currentWeather)
        currentData = response.css(currentWeatherData + 'div.pull-left table tr b::text').getall()
        #print(currentData)
        
        sevenDayForecast = 'ul.list-unstyled li.forecast-tombstone '
        weekName = response.css( sevenDayForecast + 'p.period-name::text' ).getall()
        weekCondition = response.css( sevenDayForecast + 'p.short-desc::text' ).getall()
        weekWeather = response.css( sevenDayForecast + 'p.temp::text' ).getall()
        
        #print(weekName)
        #print(weekCondition)
        #print(weekWeather)
        
        #Path(filename).write_bytes(response.css('div.panel::text'))
        #self.log(f'Saved file {filename}')
