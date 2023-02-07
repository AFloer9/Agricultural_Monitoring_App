from pathlib import Path

import scrapy

class WeatherData(scrapy.Spider):
    name = "weather"
    start_urls = [
            'https://forecast.weather.gov/MapClick.php?lat=45.63854500000008&lon=-122.64183499999996#.Y-ICRBzMKRQ'
            ]
    allowed_domains = ['forecast.weather.gov']

    def parse(self, response):
        filename = 'weather.html'
        print(response.css('div.panel::text').get())
        #Path(filename).write_bytes(response.css('div.panel::text'))
        #self.log(f'Saved file {filename}')
