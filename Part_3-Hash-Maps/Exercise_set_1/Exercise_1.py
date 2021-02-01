""" EXERCISE 1
Write a Python function that will create and return a dictionary from another
dictionary, but sorted by value. You can assume the values are all comparable
and have a natural sort order.

For example, given the following dictionary:

    composers = {'Johann': 65, 'Ludwig': 56, 'Frederic': 39, 'Wolfgang': 35}

Your function should return a dictionary that looks like the following:

    sorted_composers = {'Wolfgang': 35,
                        'Frederic': 39, 
                        'Ludwig': 56,
                        'Johann': 65}
"""


def sort_dictionary(input_dict):
    return dict(sorted(input_dict.items(), key=lambda x: x[1]))


# Testing
composers = {'Johann': 65, 'Ludwig': 56, 'Frederic': 39, 'Wolfgang': 35}

print(sort_dictionary(composers))