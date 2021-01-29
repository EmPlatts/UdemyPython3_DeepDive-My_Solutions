""" PROJECT 5
Create a conext manager that only requires the file name and provides
an iterator to iterste over the data in the file.
Iterator should yield named tuples with field names based on header rows.

Goal 1: implement a context manager using a context manager class
Goal 2: re-implement Goal 1 but using a generator function instead.
"""
import csv
from collections import namedtuple
from itertools import islice
from contextlib import contextmanager

# Goal 1:
def csv_dialect(fname):
    #Autodetect dialect of csv file
    with open(fname) as f:
        return csv.Sniffer().sniff(f.read(1000))

class IterateThroughFile:
    def __init__(self,fname):
        self.fname = fname

    def __enter__(self):
        self._f = open(self.fname, 'r')
        self._reader = csv.reader(self._f, csv_dialect(self.fname))
        header = map(lambda x: x.lower(), next(self._reader))
        self._nt = namedtuple('Data', header)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._f.close()
        return False

    def __iter__(self):
        return self

    def __next__(self):
        if self._f.closed:
            raise StopIteration
        else:
            return self._nt(*next(self._reader))

with IterateThroughFile('Data/cars.csv') as data:
    for row in islice(data, 5):
        print(row)

# Goal 2:
@contextmanager
def iterate_through_file(fname):
    f = open(fname)
    try:
        dialect = csv.Sniffer().sniff(f.read(1000))
        f.seek(0) #reset fo reader
        reader = csv.reader(f, dialect)
        header = map(lambda x: x.lower(), next(reader))
        nt = namedtuple('Data', header)
        yield (nt(*row) for row in reader)
    finally:
        f.close

with iterate_through_file('Data/cars.csv') as data:
    for row in islice(data, 5):
        print(row)