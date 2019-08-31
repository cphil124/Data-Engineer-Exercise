#!/usr/bin/env python3

import requests
import pandas as pd
import os
from tkinter import Tk, filedialog
from iso_code_dict import get_CC, get_inverse_cc


# Storing URL Endpoints for later reference
CITIES_URL = r'https://api.openaq.org/v1/cities'
SOURCES_URL = r'https://api.openaq.org/v1/sources'

CC = get_CC()
Inverse_CC = get_inverse_cc()


_root = Tk()
_root.withdraw()
direc = filedialog.askdirectory()
if direc:
    TARGET_DIRECTORY = direc
else:
    TARGET_DIRECTORY = os.getcwd()

def get_active_sources(destination=None):
    
    # URL and Payload for GET request
    url = SOURCES_URL
    payload =  {'order_by' : ['country', 'active'], 'limit' : 10000}

    # Result List Placeholders
    full_list = []
    count_dict = {}

    # GET Request + Conversion to JSON
    data = requests.get(url, params=payload)
    result_list = data.json()['results']

    # Sum Active Sources by Country
    for result in result_list:
        country = result['country']
        if result['active'] and country in count_dict.keys():
            count_dict[country] += 1
        elif result['active'] and country not in count_dict.keys():
            if country == '':
                count_dict['BLANK'] = 1
            else:
                count_dict[country] = 1

    # Add Country Name if Country Code is in Alias Dictionary
    for key in count_dict.keys():
        if key in CC.keys():
            full_list.append([key, CC[key], count_dict[key]])
    else:
        full_list.append([key, key, count_dict[key]])

    # Convert 2D List to DataFrame, push out to .csv
    frame = pd.DataFrame(full_list, columns=['Country ISO Code', 'Country', 'Active Source Count'])
    if destination:
        new_path = os.path.join(destination, 'Sources_Count.csv')
    else:
        new_path = os.path.join(os.getcwd(), 'Sources_Count.csv')
    
    frame.to_csv(new_path)
    return frame


def city_and_location_count(destination=None):

    # URL and Payload for GET request
    url = CITIES_URL
    payload = {'limit':5000}

    # Result List Placeholders
    full_list = []
    count_dict = {}

    # GET Request + Conversion to JSON
    data = requests.get(url, params=payload)
    result_list = data.json()['results']

    # Sum location and city count by country
    for result in result_list:
        country = result['country']
        locations = result['locations']
        if country in count_dict.keys():
            count_dict[country][0] += 1
            count_dict[country][1] += locations
        else:
            count_dict[country] = [1, locations]

    # Check for ISO code in dictionary and add Country name if available, and then create final dataset
    for key in count_dict.keys():
        if key in CC.keys():
            full_list.append([key, CC[key], count_dict[key][0], count_dict[key][1]])
        else:
            full_list.append([key, key, count_dict[key][0], count_dict[key][1]])
    
    
    # Create destination path for output csv
    frame = pd.DataFrame(full_list, columns=['Country ISO Code', 'Country', 'Number of Cities', 'Number of Locations'])
    if destination:
        dest_path = os.path.join(destination, 'City_Loc_Count.csv')
    else:
        dest_path = os.path.join(os.getcwd(), 'City_Loc_Count.csv')
    frame.to_csv(dest_path)
    return frame



# Get Country List input from user:
def _get_countries_input():
    _root = Tk()
    _root.withdraw()
    countries_list = []
    countries_file = filedialog.askopenfilename(title='Select Countries Text File. File Should Be 1 Country Name or ISO Code per Line ')
    with open(countries_file, 'r') as f:
        for line in f:
            countries_list.append(line.strip())
    print(countries_list)
    return countries_list
        
# print(_get_countries_input())


def get_source_urls(countries_list=None, destination=None):
    
    # Parse list of input countries and reformat to ISO codes if not already
    # Intended to handle both ISO code and country names as inputs.
    valid_country_list = []
    if not countries_list:
        country_list = _get_countries_input()
    else: 
        country_list = countries_list
    for country in country_list:
        c = country.upper()                             # Upper Case to enforce uniformity and match with dictionary
        if len(c) == 2:
            valid_country_list.append(c)
        elif len(c) > 2 and c in Inverse_CC.keys():
            valid_country_list.append(Inverse_CC[c])
        else: 
            print(f'{c} does not appear to be a valid/supported country. Please check your input list.')
    
    # Result List Placeholders
    url_dict = {}
    full_list = []
    for country in valid_country_list:
        url_dict[country] = []
    no_sources = []

    # If a premade countries list is being passed, then it is a test, so the name filename will be updated accordingly
    filename = 'Source_URLs.csv'
    if countries_list:
        filename = 'Test_' + filename

    # GET Request
    payload = {'limit':5000}
    req = requests.get(SOURCES_URL, params=payload)
    result_list = req.json()['results']

    # If result is from target country, Source URL is added to list
    for result in result_list:
        country = result['country']
        if country in valid_country_list:
            url_dict[country].append(result['sourceURL'])

    # Create final list for writing output
    for key in url_dict:
        # If country does not have any sources, a statement notifying the user will be outputted
        # and the country will be excluded from the csv output file. 
        if len(url_dict[key]) == 0:
            if key in CC.keys():
                no_sources.append(f'{CC[key]} has no sources')
            else: 
                no_sources.append(f'{key} has no sources')
        else:
            for i in range(len(url_dict[key])):
                if key in CC.keys():
                    full_list.append([key, CC[key], url_dict[key][i]])
                else:
                    full_list.append([key, key, url_dict[key][i]])
        
    frame = pd.DataFrame(full_list, columns=['Country ISO Code', 'Country', 'Source URL\'s'])

    # Check for destination argument and uses current working directory if none is found
    if destination:
        dest_path = os.path.join(destination, filename)
    else:
        dest_path = os.path.join(os.getcwd(), filename)
    
    # Output results to csv file
    frame.to_csv(dest_path)

    # All passed countries without a source url found are written into a text 
    no_sources_path = os.path.join(destination, 'Countries_without_Sources.txt')
    with open(no_sources_path, 'w') as f:
        for line in no_sources:
            f.write(line+'\n')
    return frame

TEST_LIST = ['Canada', 'Ireland', 'Japan', 'Morocco', 'Norway']
TEST_LIST2 =   ['CA', 'IE', 'JP', 'MA', 'NO']


def main():
    
    # Test Execution of each function to get result files
    get_active_sources(destination=TARGET_DIRECTORY)
    city_and_location_count(destination=TARGET_DIRECTORY)
    get_source_urls(countries_list = TEST_LIST, destination=TARGET_DIRECTORY)
    
    # Final Execution of Get Source URL's taking in User Input for countries.
    get_source_urls(destination=TARGET_DIRECTORY)

if __name__ == '__main__':
    main()


