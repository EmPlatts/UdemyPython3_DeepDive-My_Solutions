# Testing functions here

import csv
import constants
import parse_utils
import itertools
from datetime import datetime
from functools import partial

# for fname in constants.fnames:
#     print(fname)
#     with open(fname) as f:
#         reader = csv.reader(f, delimiter=',', quotechar='"')
#         print(next(reader))
#         print(next(reader))

# #header
# for fname in constants.fnames:
#     print(fname)
#     reader = parse_utils.csv_parser(fname,include_header=True)
#     print(next(reader))

# #just data
# for fname in constants.fnames:
#     print(fname)
#     reader = parse_utils.csv_parser(fname)
#     print(next(reader))
#     print(next(reader),end='\n')

# reader = parse_utils.csv_parser(constants.fname_update_status)
# for _ in range(5):
#     record = next(reader)
#     print(record[0], record[1], parse_utils.parse_date(record[1]))

# for fname, class_name, parser in zip(constants.fnames, constants.class_names, constants.parsers):
#     file_iter = parse_utils.iter_file(fname, class_name, parser)
#     print(fname)
#     for _ in range(3):
#         print(next(file_iter))

# gen = parse_utils.iter_combined_plain_tuple(constants.fnames, constants.class_names, constants.parsers, constants.compress_fields)
# print(list(next(gen)))
# print(list(next(gen)))

# nt = parse_utils.create_combo_named_tuple_class(constants.fnames, constants.compress_fields)
# print(nt._fields)

# data_iter = parse_utils.iter_combined(constants.fnames, constants.class_names, 
#                                       constants.parsers, constants.compress_fields)
# for row in itertools.islice(data_iter, 5):
#     print(row)

# Goal 3 and 4
# cutoff_date = datetime(2017,3,1)

# def group_key(item):
#     return item.gender, item.vehicle_make

# data = parse_utils.filtered_iter_combined(constants.fnames, constants.class_names, 
#                                       constants.parsers, constants.compress_fields,
#                                       key=lambda row: row.last_updated >= cutoff_date)

# sorted_data = sorted(data, key=group_key)

# groups_1 = itertools.groupby(sorted_data, key=group_key) #tee won't work here because it does a shallow copy
# groups_2 = itertools.groupby(sorted_data, key=group_key)

# group_f = (item for item in group_1 if item[0][0]=='Female')
# data_f = ((item[0][1], len(list(item[1]))) for item in group_f)

# group_m = (item for item in group_2 if item[0][0]=='Male')

# Goal 3 and 4
cutoff_date = datetime(2017,3,1)

def group_key(row):
    return row.vehicle_make

def filter_key(cutoff_date, gender, row):
    return row.last_updated >= cutoff_date and row.gender == gender


results_f = parse_utils.group_data(constants.fnames, constants.class_names, 
                                    constants.parsers, constants.compress_fields,
                                    filter_key = partial(filter_key, cutoff_date, 'Female'),
                                    group_key = lambda row: row.vehicle_make)

results_m = parse_utils.group_data(constants.fnames, constants.class_names, 
                                    constants.parsers, constants.compress_fields,
                                    filter_key = lambda row: filter_key(cutoff_date, 'Male', row),
                                    group_key = lambda row: row.vehicle_make)

print('results_f')
for row in results_f:
    print(row)

print('results_m')
for row in results_m:
    print(row)
