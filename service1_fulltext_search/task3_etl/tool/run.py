import argparse
import sqlite3

from tool.services.es_loader import ESLoader
from tool.services.etl import ETL


def run_tool():
    parser = argparse.ArgumentParser(description='Tool for loading movies data from sqlite to elastic')
    parser.add_argument('sqlite_db_path', help='Path to file with movies data in sqlite db format')

    args = parser.parse_args()

    es_loader = ESLoader('http://127.0.0.1:9200/movies')
    with sqlite3.connect(args.sqlite_db_path) as conn:
        etl = ETL(conn, es_loader)
        etl.load('movies')


if __name__ == '__main__':
    run_tool()