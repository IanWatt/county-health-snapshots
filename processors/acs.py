import setup
import os
import yaml
from pprint import pprint
from tablib import Dataset
from requests import get
from json import loads

# ex:
# https://api.census.gov/data/2017/acs/acs5/{TABLE}?get={FIELD1},{FIELD2}&for=county:*&in=state:48&key={KEY}
key = os.getenv('CENSUS_API_KEY')
base = 'https://api.census.gov/data/2017/acs/acs5'
geo = f'for=county:*&in=state:48&key={key}'

def get_url(table: str, fields: list):
    return f"{base}/{table}?get={','.join(fields)}&{geo}"

def to_dict(headers, row):
    dct = {
        header: row[i]
        for i, header
        in enumerate(headers)
    }
    dct['fips'] = f"{dct['state']}{dct['county']}"
    return dct

def to_dict_array(json: list):
    headers = json[0]
    rows = json[1:]
    return [ to_dict(headers, row) for row in rows ]

config = yaml.load(open('input/field_config.yaml').read())

queries = {} # { table: fields[] }

for dashboard in config.values():
    for heading in dashboard.values():
        for field in heading:
            source_info, field_info = field['source']
            table = source_info.split('_')[1]
            if ':' in field_info:
                fields = field_info.split(':')[1:]
            else:
                fields = [ field_info ]

            # print(f"{table}: {','.join(fields)}")

            if table not in queries:
                queries[table] = []

            query = queries[table]

            for field in fields:
                if field not in query:
                    query.append(field)

for table, fields in queries.items():
    url = get_url(table.lower(), fields)
    json = loads(get(url).text)
    dataset = Dataset()
    dataset.dict = to_dict_array(json)
    open(f'data/acs_{table.lower()}.csv', 'w', newline='').write(dataset.csv)

open('data/acs.txt', 'w').write('done')

