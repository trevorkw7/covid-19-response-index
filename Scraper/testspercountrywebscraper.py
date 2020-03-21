#importing libraries
import os.path
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests

def scrape():
    url = 'https://ourworldindata.org/coronavirus-testing-source-data'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    date_paragraphs = soup.find("div", class_ = "wp-block-column")
    data_paragraph = ""
    for paragraph in date_paragraphs:
        if(paragraph.get_text().find("we could find as of")):
            data_paragraph = paragraph

    date = paragraph.find("strong").get_text()
    date = date[date.index("f") + 2 : date.index(",")]

    #table on website
    testingTable = soup.find("div", class_ = "tableContainer")

    #all rows in table organized into a list
    itemsList = testingTable.find_all('tr')

    #remove title from itemsList
    itemsList.pop(0)

    countriesAndTests = []
    countries = []
    tests = []

    #first cell containing country name
    for item in itemsList:
        countries.append(item.find('td').get_text())
    index = 0
    #second cell via list returned containing tests
    for item in itemsList:
        tests.append(item.find_all("td")[1].get_text())

    compiled_data = pd.DataFrame(
        {
            "location": countries,
            "tests": tests,
            "dt": date
        })
    print(compiled_data)
    compiled_data.to_json('./Scraper/Data/compiled_data_ourworld.json')
