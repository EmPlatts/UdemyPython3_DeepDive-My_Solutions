""" EXERCISE 2
Given two dictionaries, d1 and d2, write a function that creates a dictionary
that contains only the keys common to both dictionaries, with values being a 
tuple containg the values from d1 and d2. (Order of keys is not important).

For example, given two dictionaries as follows:

    d1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    d2 = {'b': 20, 'c': 30, 'y': 40, 'z': 50}

Your function should return a dictionary that looks like this:
    d = {'b': (2, 20), 'c': (3, 30)}  
"""


def values_from_common_keys(d1, d2):
    common_keys = d1.keys() & d2.keys()
    return {c : (d1[str(c)], d2[str(c)]) for c in common_keys}


# Testing
d1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
d2 = {'b': 20, 'c': 30, 'y': 40, 'z': 50}

print(values_from_common_keys(d1, d2))