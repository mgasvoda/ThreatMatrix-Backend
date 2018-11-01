import pandas as pd 
import sqlalchemy
import logging
import argparse

from data_sources import acled, world_bank
from utils import upsert

log = logging.getLogger(__name__)

sources = {
    'acled': acled,
    'wbi': world_bank 
}
# TODO: clean this up
tables = {
    'acled': 'events',
    'wbi': 'country_basics'
}


def main():
    args = parse_args()
    log.info('starting')
    df = sources[args.source].get_data()
    table = tables[args.source]
    upsert(df, table)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source')
    parser.add_argument('-d', '--date', default=None)

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', action='store_const',
                           const=logging.DEBUG, default=logging.INFO)
    verbosity.add_argument('-q', '--quiet', dest='verbose',
                           action='store_const', const=logging.WARNING)

    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    main()
