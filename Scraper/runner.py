from apscheduler.schedulers.blocking import BlockingScheduler
import parsedata
import testspercountrywebscraper

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=3)
def run():
    print("execute")
    testspercountrywebscraper.scrape()
    parsedata.parse()
sched.start()
