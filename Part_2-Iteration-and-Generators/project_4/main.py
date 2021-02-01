"""PROJECT 4
Data files: personal_info.csv, vehicles.csv, employment.csv, update_status.csv

Goal 1: Create lazy iterator for each of the four data files.
Returns named tuple with correct data type.

Goal 2: Create single iterator that combines all data from Goal 1.
One row per SSN containing data from all files in a single named tuple.

Goal 3: Modify iterator from Goal 2 to filter if update state < 3/1/2017.

Goal 4: For non-stale records, generate lists of number of car makes by gender.
"""

from datetime import datetime
from functools import partial

import constants
from parse_utils import group_data

def group_key(row):
    return row.vehicle_make


def filter_key(cutoff_date, gender, row):
    return row.last_updated >= cutoff_date and row.gender == gender


cutoff_date = datetime(2017,3,1)

for gender in ('Female', 'Male'):
    results = group_data(constants.fnames, constants.class_names, 
                         constants.parsers, constants.compress_fields,
                         filter_key = partial(filter_key, cutoff_date, gender),
                         group_key = lambda row: row.vehicle_make)
    print(f'************ {gender} ************')
    print(list(results))