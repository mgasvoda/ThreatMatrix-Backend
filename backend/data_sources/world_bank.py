import requests
import pandas as pd
import collections

def get_data(): 
    base_url = 'http://api.worldbank.org/v2/countries'
    params = {
        'format': "json"
    }
    r = requests.get(base_url, params=params, verify=False)
    data = r.json()[1]
    data = [flatten(i) for i in data] 
    df = pd.DataFrame(data)
    return df


def flatten(data, parent_key='', sep='_'):
    items = []
    for k, v in data.items():
        new_key = parent_key + sep + k if parent_key else k
        try:
            items.extend(flatten(v, new_key, sep=sep).items())
        except AttributeError:
            items.append((new_key, v))
    return dict(items)
