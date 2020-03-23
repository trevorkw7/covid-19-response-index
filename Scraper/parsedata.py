import pandas as pd
import country_converter as coco
import json
from geonamescache.mappers import country
import pyrebase

#config firebase for script storage
config = {
    "apiKey": "AIzaSyB8nEOJTUEo2UAvMkGcL2PKPmBNj28Se2I",
    "authDomain": "covid-19-testing-data.firebaseapp.com",
    "databaseURL": "https://covid-19-testing-data.firebaseio.com",
    "storageBucket": "covid-19-testing-data.appspot.com",
    "serviceAccount": "service.json"
}
# print(open("service.json", "r").read())
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

def parse():


    #combining locations into an array
    with open('./compiled_data_ourworld.json') as f:
        our_world_data = json.load(f)

    countries_dict = our_world_data['location']
    tests_dict = our_world_data['tests']

    #zeros in on values in dictionary
    countries_list = list(countries_dict.values())
    tests_list = list(tests_dict.values())


    #convert tests list into integers: N/A is converted to -1
    i=0
    while(i < len(tests_list)):
        tests_list[i] = tests_list[i].replace(',','')
        if(tests_list[i].isdigit()):
            tests_list[i] = int(tests_list[i])
        else:
            tests_list[i] = -1
        i+=1

    #create ISO_3_list
    ISO_3_list = coco.convert(names = countries_list, to = 'ISO3')

    #create ISO_2_list
    ISO_2_list = coco.convert(names = ISO_3_list, to = "ISO2")
    for z in range(len(ISO_2_list)):
        ISO_2_list[z] = ISO_2_list[z].lower()

    #mapper converts iso name to population
    mapper = country(from_key='iso3', to_key='population')
    population_list = []

    #remove local data points
    index = 0
    length = len(countries_list)
    while(index < length):
        if ("–" in countries_list[index]):
            countries_list.remove(countries_list[index])
            ISO_3_list.remove(ISO_3_list[index])
            ISO_2_list.remove(ISO_2_list[index])
            tests_list.remove(tests_list[index])
            length = length - 1
            continue
        index += 1

    #create population list
    j=0
    while(j < len(ISO_3_list)):
        population_list.append(mapper(ISO_3_list[j]))
        j+=1


    #fix duplicates - add tests in same country together
    #
    # l=0
    # m=1
    # length = len(ISO_3_list)
    # while (m < length):
    #     if(ISO_3_list[l] == ISO_3_list[m]):
    #         total = tests_list[l] + tests_list[m]
    #         tests_list[l] = total
    #         tests_list[m] = total
    #         length -= 1
    #     l += 1
    #     m += 1

    #tpc - tests per million people = (tests/population) * million
    tpc_list = []
    #create tests per million list
    k=0
    while(k < len(tests_list)):
        tpc_list.append(round(tests_list[k]/population_list[k] * 1000000))
        k+=1

    # #fix duplicates - remove diplicate entries
    # n=0
    # o=1
    # length = len(ISO_3_list)
    # while (o < length):
    #     if(ISO_3_list[n] == ISO_3_list[o]):
    #         del ISO_3_list[n]
    #         del population_list[n]
    #         del tests_list[n]
    #         del tpc_list[n]
    #         length -= 1
    #     n += 1
    #     o += 1

    #create lattitude and longitude list
    location_lat=[]
    location_long=[]
    with open('countrycode-latlong.json') as g:
        lat_long_data = json.load(g)

    for iso2_code in ISO_2_list:
        location_lat.append(lat_long_data[iso2_code]["lat"])
        location_long.append(lat_long_data[iso2_code]["long"])

    #create dataframe and export
    compiled_data = pd.DataFrame(
        {
            "location": countries_list,
            "location_code": ISO_3_list,
            "location_lat": location_lat,
            "location_long": location_long,
            "location_pop": population_list,
            "tests": tests_list,
            "tests_per_million": tpc_list
        })

    print(compiled_data)
    compiled_data.to_json('./our_world_parsed.json', orient='records')
    storage.child('/')
    storage.child('our_world_parsed.json').put('./our_world_parsed.json')

def parse_hopkins(file_name):

        with open(file_name) as f:
            hopkins_data = json.load(f)

        #contains other (numbered) dictionaries that contain the info
        hopkins_data_dict = hopkins_data['data']

        #data lists
        countries_list = []
        confirmed_list = []
        deaths_list = []
        recovered_list = []

        #add info to the corresponding lists
        for i in range(0, len(hopkins_data_dict)):
            countries_list.append(hopkins_data_dict[str(i)]['location'])
            confirmed_list.append(hopkins_data_dict[str(i)]['confirmed'])
            deaths_list.append(hopkins_data_dict[str(i)]['deaths'])
            recovered_list.append(hopkins_data_dict[str(i)]['recovered'])

        ISO_3_list = coco.convert(names = countries_list, to = 'ISO3')

        compiled_data = pd.DataFrame(
            {
                "location_code": ISO_3_list,
                "confirmed_cases": confirmed_list,
                "deaths": deaths_list,
                "recovered": recovered_list,
                "dt": file_name[37:-5]
            })

        print(compiled_data)
        #substring includes the date and time of the file
        compiled_data.to_json('./Scraper/Data/parsed_data_' + file_name[29:])

#file1 should have earlier data than file2
def calculate_growth(file1, file2):
    with open(file1) as f:
        data_json_1 = json.load(f)

    with open(file2) as f:
        data_json_2 = json.load(f)

    locations_list = []
    recovered_growth_list = []
    confirmed_growth_list = []
    deaths_growth_list = []

    countries_dict = data_json_1["location_code"]
    locations_list = list(countries_dict.values())

    for i in range(0, len(locations_list)):
        recovered_growth = int(data_json_1["recovered"][str(i)]) - int(data_json_2["recovered"][str(i)])
        recovered_growth_list.append(recovered_growth)

        confirmed_growth = int(data_json_1["confirmed_cases"][str(i)]) - int(data_json_2["confirmed_cases"][str(i)])
        confirmed_growth_list.append(confirmed_growth)

        deaths_growth = int(data_json_1["deaths"][str(i)]) - int(data_json_2["deaths"][str(i)])
        deaths_growth_list.append(deaths_growth)

    compiled_growth_data = pd.DataFrame(
    {
        "location_code": locations_list,
        "recovered_growth": recovered_growth_list,
        "confirmed_cases_growth": confirmed_growth_list,
        "deaths_growth": deaths_growth_list
    })

    print(compiled_growth_data)
    compiled_growth_data.to_json('./Scraper/Data/growth_data.json')
