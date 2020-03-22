from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import pandas as pd
import io
import requests

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours = 1)
def collect_data():
    print("Collecting data")
    url="https://covid2019-api.herokuapp.com/v2/current"
    s=requests.get(url).content
    c=pd.read_json(io.StringIO(s.decode('utf-8')))

    #retrieve time stamp and create json file
    now = datetime.now()
    file_name = "./Scraper/Data/compiled_data_hopkins_" + now.strftime("%Y-%m-%d_%Hh%Mm%Ss") + ".json"
    c.to_json(file_name)

sched.start()

#print("Data retrieved - " + now.strftime("%B %d, %Y %I:%M:%S %p %Z"))
