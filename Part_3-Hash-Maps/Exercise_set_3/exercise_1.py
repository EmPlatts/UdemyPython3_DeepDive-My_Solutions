""" EXERCISE 1
Let's revisit an exercise we did right after the section on dictionaries.

You have text data spread across multiple servers. Each server is able to
analyze this data and return a dictionary that contains words and their 
frequency. Your job is to combine this data to create a single dictionary that
contains all the words and their combined frequencies from all these data
sources. Bonus points if you can make your dictionary sorted by frequency (highest to lowest).

Implement two different solutions to this problem:

a: Using defaultdict objects

b: Using Counter objects
"""

d1 = {'python': 10, 'java': 3, 'c#': 8, 'javascript': 15}
d2 = {'java': 10, 'c++': 10, 'c#': 4, 'go': 9, 'python': 6}
d3 = {'erlang': 5, 'haskell': 2, 'python': 1, 'pascal': 1}

# a)
from collections import defaultdict

def merge_using_defaultdict(*dicts):
    total = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            total[k] += v
    return dict(sorted(total.items(), key=lambda x: x[1], reverse=True))

print(merge_using_defaultdict(d1,d2,d3))


# b)
from collections import Counter

def merge_using_Counter(*dicts):
    counter = Counter()
    for d in dicts:
        counter += d
    return dict(counter.most_common())

print(merge_using_Counter(d1,d2,d3))


