""" EXERCISE 3
You have text data spread across multiple servers. Each server is able to
analyze this data and return a dictionary that contains words and their 
frequency.

Your job is to combine this data to create a single dictionary that contains
all the words and their combined frequencies from all these data sources.

Bonus points if you can make your dictionary sorted by freq (high to low).

For example, you may have three servers that each return these dictionaries:

    d1 = {'python': 10, 'java': 3, 'c#': 8, 'javascript': 15}
    d2 = {'java': 10, 'c++': 10, 'c#': 4, 'go': 9, 'python': 6}
    d3 = {'erlang': 5, 'haskell': 2, 'python': 1, 'pascal': 1}

Your resulting dictionary should look like this:

    d = {'python': 17,
        'javascript': 15,
        'java': 13,
        'c#': 12,
        'c++': 10,
        'go': 9,
        'erlang': 5,
        'haskell': 2,
        'pascal': 1}

If only servers 1 and 2 return data (so d1 and d2), results would look like:

    d = {'python': 16,
        'javascript': 15,
        'java': 13,
        'c#': 12,
        'c++': 10, 
        'go': 9}

"""


def find_frequency_in_dicts(*dicts):

    def sort_dictionary(input_dict):
        return dict(sorted(input_dict.items(), key=lambda x: x[1], reverse=True))

    keys = set().union(*dicts)
    counts = dict()
    for key in keys:
        count = 0
        for d in dicts:
            count += d.get(key, 0)
        counts[key] = count
    
    return sort_dictionary(counts)


# Testing
d1 = {'python': 10, 'java': 3, 'c#': 8, 'javascript': 15}
d2 = {'java': 10, 'c++': 10, 'c#': 4, 'go': 9, 'python': 6}
d3 = {'erlang': 5, 'haskell': 2, 'python': 1, 'pascal': 1}

print(find_frequency_in_dicts(d1,d2,d3))