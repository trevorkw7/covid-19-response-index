import pandas as pd
import country_converter as coco
import json
from geonamescache.mappers import country

def parse():
    #tpc - tests per million people = (tests/population) * million
    tpc_list = []

    #combining locations into an array
    with open('./Scraper/Data/compiled_data_ourworld.json') as f:
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


    ISO_3_list = coco.convert(names = countries_list, to = 'ISO3')

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

    #create tests per million list
    k=0
    while(k < len(tests_list)):
        tpc_list.append(tests_list[k]/population_list[k] * 1000000)
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

    compiled_data = pd.DataFrame(
        {
            "location_code": ISO_3_list,
            "location_pop": population_list,
            "tests": tests_list,
            "tests_per_million": tpc_list
        })

    print(compiled_data)
    compiled_data.to_json('./Scraper/Data/parsed_data.json')
