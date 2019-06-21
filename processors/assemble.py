import setup
import yaml
from tablib import Dataset

config = yaml.load(open('input/field_config.yaml').read())
counties = Dataset().load(open('input/geographies.csv').read()).dict

# source id:
#   county fips:
#       field: value
sources = {}

def get_value(source, fips, field):
    if source not in sources:
        data = Dataset().load(open(f'data/{source}.csv').read())
        sources[source] = {
            row['fips']: row
            for row in data.dict
        }

    return float(sources[source][fips][field]) or 0

# output schema:
# County Name, County FIPS Code, Variable Name, County Value, Value Type

rows = []

def get_interpreted_value(source, field_info, fips):
    if ':' in field_info:
        arr = field_info.split(':')
        op = arr[0]
        values = [
            get_value(source, fips, field)
            for field in arr[1:]
        ]
        if op == 'INVERT':
            return 100 - float(values[0])
        elif op == 'SUM':
            return sum(values)
        else:
            raise Exception('invalid operaton')
    else:
        return get_value(source, fips, field_info)


for dashboard, headings in config.items():
    for heading, fields in headings.items():
        for field in fields:
            for county in counties:
                fips = county['fips']

                value = get_interpreted_value(
                    *field['source'], fips
                )

                rows.append({
                    'County Name': county['name'],
                    'County FIPS Code': fips,
                    'Variable Name': field['name'],
                    'County Value': value,
                    'Value Type': 'Percent' # could be dynamic
                })

final = Dataset()
final.dict = rows
open('data/final.csv', 'w', newline='\n').write(final.csv)