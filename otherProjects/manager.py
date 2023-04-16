# Author: Alexander Flores Spring 2023 Class: CS 320
import subprocess
import csv
import os

def weatherToCSV(filename):
    with open(filename +'.txt', 'r') as file:
        with open(filename + '.csv', 'w') as f:
            csv_write = csv.writer(f, delimiter='\t')
            for line in file:
                csv_write.writerow(line[1:-2].replace("'", '').split(','))


def scrapy_data():
    # scrapy
    filename = 'weatherData'
    with open(filename + '.txt', 'w') as file:
        subprocess.run(['scrapy','crawl', 'weather','-s','LOG_ENABLED=False'], stdout=file)
        weatherToCSV(filename)

        os.remove(filename + '.txt')


def arduino_data():
    pass


scrapy_data()
