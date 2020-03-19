import time
from timeloop import Timeloop
from datetime import timedelta
import parsedata
import testspercountrywebscraper

t1 = Timeloop()

@t1.job(interval=timedelta(seconds=1))
def run():
    print("execute")
    testspercountrywebscraper.scrape()
    parsedata.parse()

if __name__ == "__main__":
    t1.start(block=True)
