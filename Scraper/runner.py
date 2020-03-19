import time
import parsedata
import testspercountrywebscraper

def run():
    testspercountrywebscraper.scrape()
    parsedata.parse()

while True:
    print("execute")
    run()
    time.sleep(10)
