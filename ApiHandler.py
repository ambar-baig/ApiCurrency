from configparser import ConfigParser
import requests
import os
import time
import csv
import json


API_URL = ""
API_FUNCTION = ""
API_PARA_PATH = ""
API_KEY = ""


def load_config(filename='api.ini'):
    global API_URL, API_FUNCTION, API_PARA_PATH, API_KEY
    config_handler = ConfigParser()
    config_handler.read(filename)
    API_URL = config_handler['API_CONFIG']['API_URL']
    API_FUNCTION = config_handler['API_CONFIG']['API_FUNCTION']
    API_PARA_PATH = config_handler['API_CONFIG']['API_PARA_PATH']
    API_KEY = config_handler['API_CONFIG']['API_KEY']
    
def fetch_data(url):
    response = requests.get(url)
    print(response.text)
    return response.text
    
    
def load_country_currency_symbol(filename):
    data_list= []
    with open(filename, 'r') as fileHandler:
        csv_dict_handler = csv.DictReader(fileHandler)
        for csv_dict in csv_dict_handler:
            data = (csv_dict['currency code'], csv_dict['currency name'])
            data_list.append(data)
    return data_list

def convert_crypto_to_other_currency(countries):
    data = []
    i = 1
    for country in countries:
        data.append([country,json.loads(fetch_data(API_URL.format(API_FUNCTION,country[0],  API_KEY)))['Realtime Currency Exchange Rate']['8. Bid Price']])
        i = i + 1
        if i % 5 == 0:
            time.sleep(60 * 2)
            i = 1
            break
            
    return data
        

if __name__ == '__main__':
    load_config()
    print(f'API KEY => {API_URL}')
    print(f'API URL => {API_FUNCTION}')
    print(f'API REQ PARA => {API_PARA_PATH}')
    print(f'API KEY => {API_KEY}')
    print(convert_crypto_to_other_currency(load_country_currency_symbol(API_PARA_PATH)))
    
    
    
