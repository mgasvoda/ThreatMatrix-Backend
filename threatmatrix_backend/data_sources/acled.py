import requests
import pandas as pd

from io import StringIO
from threatmatrix_backend.utils import conn

class Acled: 

    def __init__(self):
        self.name = 'acled'
        self.table = 'events'
        self.data = None 
        self.steps = [
            self.aggregate
        ]

    def get_data(self):
        base_url = "https://api.acleddata.com/acled/read.csv"
        params = {
            "limit": 2000
        }

        # NOTE: setting verify to false is STRONGLY discouraged
        # This setting is only used in development due to restrictions
        # In my current environement, and should be disabled whenever possible
        r = requests.get(base_url, params=params, verify=False)
        wrap = StringIO(r.text)
        df = pd.read_csv(wrap)

        # A few of the sources are stored as bytestrings when the rows are converted
        # to dicts and handled individually, causing errors on insert. This is a slow,
        # but simple way to clean those out.

        df['source'] = df['source'].map(self.clean)
        self.data = df

    @staticmethod
    def clean(x):
        try:
            return x.decode('utf-8')
        except AttributeError:
            return x

    def aggregate(self):
        output_table = "acled_aggregates"
        df = self.data

        df['fatalities'] = pd.to_numeric(df['fatalites'], downcast='integer').fillna(0)
        df = df.groupby('country').sum()[fatalities].to_frame().reset_index()
        df.to_sql(output_table, conn, if_exists='replace')
