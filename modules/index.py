from typing import Generator, Iterable
from elasticsearch import Elasticsearch

import csv

es = Elasticsearch([
    'http://localhost:9200'
])
ES_INDEX = 'flatz'

def read_csv(file: Iterable[str]) -> Generator:
    reader = csv.DictReader(file, delimiter=";", skipinitialspace=True)
    for row in reader:
        yield strip(row)
        

def strip(row: dict) -> dict:
    return { k.strip(): v.strip() for k,v in row.items() }

def index(file) -> tuple[int, int]:
    created = 0
    updated = 0
    for row in read_csv(file):
        response = es.index(index=ES_INDEX, document=row, id=row['offer_id'])
        result = response.body['result']
        if result == 'created':
            created+=1
        elif result == 'updated':
            updated+=1
        else:
            raise ValueError(f'Unexpected result type: {result}')
    return created, updated