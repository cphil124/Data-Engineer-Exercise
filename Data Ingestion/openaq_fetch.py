import requests
import pandas as pd
import os
from tkinter import Tk, filedialog


# Country ISO Code Dictionary below taken from Dimitris Karagkasidis, https://github.com/pageflt
CC = {
    "AF": "AFGHANISTAN",
    "AX": "ÅLAND ISLANDS",
    "AL": "ALBANIA",
    "DZ": "ALGERIA",
    "AS": "AMERICAN SAMOA",
    "AD": "ANDORRA",
    "AO": "ANGOLA",
    "AI": "ANGUILLA",
    "AQ": "ANTARCTICA",
    "AG": "ANTIGUA AND BARBUDA",
    "AR": "ARGENTINA",
    "AM": "ARMENIA",
    "AW": "ARUBA",
    "AU": "AUSTRALIA",
    "AT": "AUSTRIA",
    "AZ": "AZERBAIJAN",
    "BS": "BAHAMAS",
    "BH": "BAHRAIN",
    "BD": "BANGLADESH",
    "BB": "BARBADOS",
    "BY": "BELARUS",
    "BE": "BELGIUM",
    "BZ": "BELIZE",
    "BJ": "BENIN",
    "BM": "BERMUDA",
    "BT": "BHUTAN",
    "BO": "BOLIVIA, PLURINATIONAL STATE OF",
    "BQ": "BONAIRE, SINT EUSTATIUS AND SABA",
    "BA": "BOSNIA AND HERZEGOVINA",
    "BW": "BOTSWANA",
    "BV": "BOUVET ISLAND",
    "BR": "BRAZIL",
    "IO": "BRITISH INDIAN OCEAN TERRITORY",
    "BN": "BRUNEI DARUSSALAM",
    "BG": "BULGARIA",
    "BF": "BURKINA FASO",
    "BI": "BURUNDI",
    "KH": "CAMBODIA",
    "CM": "CAMEROON",
    "CA": "CANADA",
    "CV": "CAPE VERDE",
    "KY": "CAYMAN ISLANDS",
    "CF": "CENTRAL AFRICAN REPUBLIC",
    "TD": "CHAD",
    "CL": "CHILE",
    "CN": "CHINA",
    "CX": "CHRISTMAS ISLAND",
    "CC": "COCOS (KEELING) ISLANDS",
    "CO": "COLOMBIA",
    "KM": "COMOROS",
    "CG": "CONGO",
    "CD": "CONGO, THE DEMOCRATIC REPUBLIC OF THE",
    "CK": "COOK ISLANDS",
    "CR": "COSTA RICA",
    "CI": "CÔTE D'IVOIRE",
    "HR": "CROATIA",
    "CU": "CUBA",
    "CW": "CURAÇAO",
    "CY": "CYPRUS",
    "CZ": "CZECH REPUBLIC",
    "DK": "DENMARK",
    "DJ": "DJIBOUTI",
    "DM": "DOMINICA",
    "DO": "DOMINICAN REPUBLIC",
    "EC": "ECUADOR",
    "EG": "EGYPT",
    "SV": "EL SALVADOR",
    "GQ": "EQUATORIAL GUINEA",
    "ER": "ERITREA",
    "EE": "ESTONIA",
    "ET": "ETHIOPIA",
    "FK": "FALKLAND ISLANDS (MALVINAS)",
    "FO": "FAROE ISLANDS",
    "FJ": "FIJI",
    "FI": "FINLAND",
    "FR": "FRANCE",
    "GF": "FRENCH GUIANA",
    "PF": "FRENCH POLYNESIA",
    "TF": "FRENCH SOUTHERN TERRITORIES",
    "GA": "GABON",
    "GM": "GAMBIA",
    "GE": "GEORGIA",
    "DE": "GERMANY",
    "GH": "GHANA",
    "GI": "GIBRALTAR",
    "GR": "GREECE",
    "GL": "GREENLAND",
    "GD": "GRENADA",
    "GP": "GUADELOUPE",
    "GU": "GUAM",
    "GT": "GUATEMALA",
    "GG": "GUERNSEY",
    "GN": "GUINEA",
    "GW": "GUINEA-BISSAU",
    "GY": "GUYANA",
    "HT": "HAITI",
    "HM": "HEARD ISLAND AND MCDONALD ISLANDS",
    "VA": "HOLY SEE (VATICAN CITY STATE)",
    "HN": "HONDURAS",
    "HK": "HONG KONG",
    "HU": "HUNGARY",
    "IS": "ICELAND",
    "IN": "INDIA",
    "ID": "INDONESIA",
    "IR": "IRAN, ISLAMIC REPUBLIC OF",
    "IQ": "IRAQ",
    "IE": "IRELAND",
    "IM": "ISLE OF MAN",
    "IL": "ISRAEL",
    "IT": "ITALY",
    "JM": "JAMAICA",
    "JP": "JAPAN",
    "JE": "JERSEY",
    "JO": "JORDAN",
    "KZ": "KAZAKHSTAN",
    "KE": "KENYA",
    "KI": "KIRIBATI",
    "KP": "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF",
    "KR": "KOREA, REPUBLIC OF",
    "KW": "KUWAIT",
    "KG": "KYRGYZSTAN",
    "LA": "LAO PEOPLE'S DEMOCRATIC REPUBLIC",
    "LV": "LATVIA",
    "LB": "LEBANON",
    "LS": "LESOTHO",
    "LR": "LIBERIA",
    "LY": "LIBYA",
    "LI": "LIECHTENSTEIN",
    "LT": "LITHUANIA",
    "LU": "LUXEMBOURG",
    "MO": "MACAO",
    "MK": "MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF",
    "MG": "MADAGASCAR",
    "MW": "MALAWI",
    "MY": "MALAYSIA",
    "MV": "MALDIVES",
    "ML": "MALI",
    "MT": "MALTA",
    "MH": "MARSHALL ISLANDS",
    "MQ": "MARTINIQUE",
    "MR": "MAURITANIA",
    "MU": "MAURITIUS",
    "YT": "MAYOTTE",
    "MX": "MEXICO",
    "FM": "MICRONESIA, FEDERATED STATES OF",
    "MD": "MOLDOVA, REPUBLIC OF",
    "MC": "MONACO",
    "MN": "MONGOLIA",
    "ME": "MONTENEGRO",
    "MS": "MONTSERRAT",
    "MA": "MOROCCO",
    "MZ": "MOZAMBIQUE",
    "MM": "MYANMAR",
    "NA": "NAMIBIA",
    "NR": "NAURU",
    "NP": "NEPAL",
    "NL": "NETHERLANDS",
    "NC": "NEW CALEDONIA",
    "NZ": "NEW ZEALAND",
    "NI": "NICARAGUA",
    "NE": "NIGER",
    "NG": "NIGERIA",
    "NU": "NIUE",
    "NF": "NORFOLK ISLAND",
    "MP": "NORTHERN MARIANA ISLANDS",
    "NO": "NORWAY",
    "OM": "OMAN",
    "PK": "PAKISTAN",
    "PW": "PALAU",
    "PS": "PALESTINE, STATE OF",
    "PA": "PANAMA",
    "PG": "PAPUA NEW GUINEA",
    "PY": "PARAGUAY",
    "PE": "PERU",
    "PH": "PHILIPPINES",
    "PN": "PITCAIRN",
    "PL": "POLAND",
    "PT": "PORTUGAL",
    "PR": "PUERTO RICO",
    "QA": "QATAR",
    "RE": "RÉUNION",
    "RO": "ROMANIA",
    "RU": "RUSSIAN FEDERATION",
    "RW": "RWANDA",
    "BL": "SAINT BARTHÉLEMY",
    "SH": "SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA",
    "KN": "SAINT KITTS AND NEVIS",
    "LC": "SAINT LUCIA",
    "MF": "SAINT MARTIN (FRENCH PART)",
    "PM": "SAINT PIERRE AND MIQUELON",
    "VC": "SAINT VINCENT AND THE GRENADINES",
    "WS": "SAMOA",
    "SM": "SAN MARINO",
    "ST": "SAO TOME AND PRINCIPE",
    "SA": "SAUDI ARABIA",
    "SN": "SENEGAL",
    "RS": "SERBIA",
    "SC": "SEYCHELLES",
    "SL": "SIERRA LEONE",
    "SG": "SINGAPORE",
    "SX": "SINT MAARTEN (DUTCH PART)",
    "SK": "SLOVAKIA",
    "SI": "SLOVENIA",
    "SB": "SOLOMON ISLANDS",
    "SO": "SOMALIA",
    "ZA": "SOUTH AFRICA",
    "GS": "SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS",
    "SS": "SOUTH SUDAN",
    "ES": "SPAIN",
    "LK": "SRI LANKA",
    "SD": "SUDAN",
    "SR": "SURINAME",
    "SJ": "SVALBARD AND JAN MAYEN",
    "SZ": "SWAZILAND",
    "SE": "SWEDEN",
    "CH": "SWITZERLAND",
    "SY": "SYRIAN ARAB REPUBLIC",
    "TW": "TAIWAN, PROVINCE OF CHINA",
    "TJ": "TAJIKISTAN",
    "TZ": "TANZANIA, UNITED REPUBLIC OF",
    "TH": "THAILAND",
    "TL": "TIMOR-LESTE",
    "TG": "TOGO",
    "TK": "TOKELAU",
    "TO": "TONGA",
    "TT": "TRINIDAD AND TOBAGO",
    "TN": "TUNISIA",
    "TR": "TURKEY",
    "TM": "TURKMENISTAN",
    "TC": "TURKS AND CAICOS ISLANDS",
    "TV": "TUVALU",
    "UG": "UGANDA",
    "UA": "UKRAINE",
    "AE": "UNITED ARAB EMIRATES",
    "GB": "UNITED KINGDOM",
    "US": "UNITED STATES",
    "UM": "UNITED STATES MINOR OUTLYING ISLANDS",
    "UY": "URUGUAY",
    "UZ": "UZBEKISTAN",
    "VU": "VANUATU",
    "VE": "VENEZUELA, BOLIVARIAN REPUBLIC OF",
    "VN": "VIET NAM",
    "VG": "VIRGIN ISLANDS, BRITISH",
    "VI": "VIRGIN ISLANDS, U.S.",
    "WF": "WALLIS AND FUTUNA",
    "EH": "WESTERN SAHARA",
    "YE": "YEMEN",
    "ZM": "ZAMBIA",
    "ZW": "ZIMBABWE",
}
# Inverse of the ISO Code dictionary for reversing conversion
Inverse_CC = {}
for item in CC.items():
    Inverse_CC[item[1]] = item[0]


# Storing URL Endpoints for later reference
CITIES_URL = r'https://api.openaq.org/v1/cities'
SOURCES_URL = r'https://api.openaq.org/v1/sources'


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


