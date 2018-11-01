import logging
import os
import time
import itertools

import sqlalchemy
import pandas as pd
import numpy as np

from sqlalchemy import exc
from db import db_location

log = logging.getLogger(os.path.dirname(__file__))
engine = sqlalchemy.create_engine(db_location)
conn = engine.connect()


def upsert(df, table, index=None):
    log.info('inserting...')
    with engine.connect() as conn:
        # log.info(df.dtypes)
        metadata = sqlalchemy.MetaData(engine)
        metadata.reflect()
        table = metadata.tables[table]
        df = df.where((pd.notnull(df)), None)

        if len(df) == 0:
            log.info('Nothing new to add')
            return

        else:
            fields = df.columns
            placeholders = ':'+', :'.join(fields)
            insert_stmt = "INSERT INTO {table} ({fields}) VALUES ({values});"\
                .format(table=table, fields=', '.join(i for i in fields), 
                        values=placeholders)

            # A seperate transaction for each record is very slow, but currently
            # Sqlalchemy doesn't support the new ON CONFLICT syntax for checking
            # batch inserts, so to avoid duplication or complete failure, this 
            # seems to be the only option for now. 
            # TODO: Convert to postgres for batch inserts
            for line in records: 
                try:
                    conn.execute(insert_stmt, **line)
                except exc.IntegrityError:
                    pass
                time.sleep(1)
                
