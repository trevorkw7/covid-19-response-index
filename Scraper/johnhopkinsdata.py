import pandas as pd
import io
import requests

url="https://covid2019-api.herokuapp.com/v2/current"
s=requests.get(url).content
c=pd.read_json(io.StringIO(s.decode('utf-8')))
c.to_json('compiled_data_hopkins.json')
