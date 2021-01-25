"""
PROJECT 3
Create a lazy iterator that produces a named tuple for each row of data.
Calculate the number of violations by car make.
Store make and violation count in a dictionary.
"""

from collections import namedtuple
from datetime import datetime
from functools import partial
from collections import defaultdict

data_file = 'data/nyc_parking_tickets_extract.csv'

with open(data_file) as f:
    headers = next(f).strip('\n').split(',')

column_names = [heading.replace(' ', '_').lower() for heading in headers]
TrafficViolation = namedtuple('TrafficViolation', column_names)

#data reader
def read_data():
    with open(data_file) as f:
        next(f) #skip header
        yield from f

#create parsers
def parse_int(value, *, default=None):
    try:
        return int(value)
    except ValueError:
        return default

def parse_date(value, *, default=None):
    date_format = '%m/%d/%Y'
    try:
        return datetime.strptime(value, date_format).date()
    except ValueError:
        return default

def parse_string(value, *, default=None):
    try:
        cleaned = value.strip()
        if not cleaned:
            return default
        else:
            return cleaned
    except ValueError:
        return default

column_parsers = (parse_int,
                  parse_string,
                  partial(parse_string,default=''),
                  partial(parse_string,default=''),
                  parse_date,
                  parse_int,
                  partial(parse_string,default=''),
                  parse_string,
                  partial(parse_string,default='')
                  )
 
def parse_row(row, *, default=None):
    fields = row.strip('\n').split(',')
    parsed_data = [func(field) for func, field in zip(column_parsers, fields)]
    #only want to retain rows which aren't missing crucial info (e.g. vehicle_make):
    if all(item is not None for item in parsed_data):
        return TrafficViolation(*parsed_data)
    else:
        return default

#create generator
def parsed_data():
    for row in read_data():
        parsed = parse_row(row)
        if parsed:
            yield parsed

#test
parsed_rows = parsed_data()
for _ in range(5):
    print(next(parsed_rows))

# #calulate number of violations by car make
# car_make_count = {}

# for data in parsed_data():
#     if data.vehicle_make in car_make_count:
#         car_make_count[data.vehicle_make] += 1
#     else:
#         car_make_count[data.vehicle_make] = 1

# for make, count in sorted(car_make_count.items(),
#                             key=lamdba t: t[1],
#                             reverse=True)

# #using defaultdict instead:
# car_make_count = defaultdict(int)

# for data in parsed_data():
#     car_make_count[data.vehicle_make] += 1

def violation_count():
    car_make_count = defaultdict(int)
    for data in parsed_data():
        car_make_count[data.vehicle_make] += 1
    return {make : count for make, count
            in sorted(car_make_count.items(),
                            key=lambda t: t[1],
                            reverse=True) }

print(violation_count())



