import pandas as pd 
import sqlalchemy
import logging
import argparse

from data_sources import acled, world_bank
from utils import upsert

log = logging.getLogger(__name__)


sources = {
    'acled': acled.Acled,
    'world_bank': world_bank.WorldBank
}


def main():
    args = parse_args()
    source = sources[args.source]()
    log.info(f'Running {source.name}')
    source.get_data()
    log.info(f'Retrieved {len(source.data)} records')
    upsert(source.data, source.table)
    if source.steps:
        for step in source.steps:
            step()


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
