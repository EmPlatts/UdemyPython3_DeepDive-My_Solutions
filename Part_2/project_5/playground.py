import csv

fnames = 'Data/cars.csv', 'Data/personal_info.csv'

for fname in fnames:
    with open(fname) as f:
        print(next(f), end='')
        print(next(f), end='')
    print('-----------')

with open(fnames[0]) as f:
    dialect = csv.Sniffer().sniff(f.read(1000))
print(vars(dialect))