import requests
import pandas as pd
import collections
import logging

from pathlib import Path

log = logging.getLogger(Path(__file__).stem)


class WorldBank:

    def __init__(self): 
        self.name = 'world_bank'
        self.table = 'country_full'
        self.data = None 
        self.steps = None

    def get_data(self): 
        base_url = 'http://api.worldbank.org/v2/countries/all/indicators/'
        series_codes = ['NY.ADJ.NNTY.PC.CD', 'NY.ADJ.DKAP.CD', 'NY.ADJ.AEDU.CD',
            'NY.ADJ.NNAT.CD', 'AG.LND.AGRI.ZS', 'VC.BTL.DETH',
            'GC.DOD.TOTL.GD.ZS', 'SP.REG.BRTH.RU.ZS', 'SP.REG.BRTH.UR.ZS',
            'FP.CPI.TOTL', 'per_si_allsi.cov_pop_tot',
            'per_sa_allsa.cov_pop_tot', 'SH.XPD.CHEX.GD.ZS', 'IC.BUS.EASE.XQ',
            'SE.TER.CUAT.BA.ZS', 'SL.EMP.TOTL.SP.MA.ZS', 'NE.EXP.GNFS.ZS',
            'BX.KLT.DINV.WD.GD.ZS', 'AG.LND.FRST.ZS', 'NY.GDP.PCAP.KD',
            'NY.GDP.MKTP.CD', 'NY.GDP.PCAP.PP.CD', 'SI.DST.10TH.10',
            'IT.NET.USER.ZS', 'SL.TLF.ACTI.ZS', 'SE.ADT.LITR.MA.ZS', 
            'MS.MIL.XPND.GD.ZS', 'SH.STA.BASS.ZS', 'SP.POP.TOTL.MA.ZS'
        ]
        params = {
            'format': "json",
            'page': 1,
            'date': '2015:2015'
        }

        full_df = pd.DataFrame(columns=['indicator', 'country', 'value'])
        for code in series_codes:
            r = requests.get(base_url + code, params=params, verify=False)
            json = r.json()[1]
            meta = r.json()[0]
            log.info(f'retrieving {code}: {meta["pages"]} to go')

            data = [self.flatten(i) for i in json] 
            df = pd.DataFrame(data)[['indicator_value', 'country_value', 'value']]
            df.rename({'indicator_value': 'indicator',
                       'country_value': 'country'}, axis=1, inplace=True)
    
            for i in range(meta['pages']-1):
                params['page'] = i+2 
                r = requests.get(base_url + code, params=params, verify=False)
                data = r.json()[1]
                data = pd.DataFrame([self.flatten(i) for i in data])
                df = df.append(data)

            full_df.append(df)
            params['page'] = 1

        self.data = df.unstack('indicator')

    def flatten(self, data, parent_key='', sep='_'):
        items = []
        for k, v in data.items():
            new_key = parent_key + sep + k if parent_key else k
            try:
                items.extend(self.flatten(v, new_key, sep=sep).items())
            except AttributeError:
                items.append((new_key, v))
        return dict(items)
