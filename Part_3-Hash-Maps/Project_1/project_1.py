""" PROJECT 1
In this project our goal is to validate one dictionary structure against a
template dictionary.

A typical example of this might be working with JSON data inputs in an API. You
are trying to validate this received JSON against some kind of template to make
sure the received JSON conforms to that template (i.e. all the keys and 
structure are identical - value types being important, but not the value itself
- so just the structure, and the data type of the values).

To keep things simple we'll assume that values can be either single values
(like an integer, string, etc), or a dictionary, itself only containing single
values or other dictionaries, recursively. In other words, we're not going to
deal with lists as possible values. Also, to keep things simple, we'll assume
that all keys are required, and that no extra keys are permitted.

In practice we would not have these simplifying assumptions, and although we
could definitely write this ourselves, there are many 3rd party libraries that
already exist to do this (such as jsonschema, marshmallow, and many more, some
of which I'll cover lightly in some later videos.)

Write a function such this:

    def validate(data, template):
        # implement
        # and return True/False
        # in the case of False, return a string describing 
        # the first error encountered
        # in the case of True, string can be empty
        return state, error

That should return this:

    validate(john, template) --> True, ''
    validate(eric, template) --> False, 'mismatched keys: bio.birthplace.city'
    validate(michael, template) --> False, 'bad type: bio.dob.month'
    
Better yet, use exceptions instead of return codes and strings!
"""

def check_keys(data, template, path):
    template_keys = template.keys()
    data_keys = data.keys()

    excess_keys = data_keys - template_keys
    missing_keys = template_keys - data_keys
    
    if excess_keys:
        raise Exception('Excess keys: ' + ', '.join({path + '.' + str(key)
                        for key in missing_keys}))
    if missing_keys:
        raise Exception('Missing keys at ' + ', '.join({path + '.' + str(key)
                        for key in missing_keys}))
    
    
def check_data_type(data, template, path):
    for key, value in template.items():
        if isinstance(value, dict):
            template_type = dict
        else:
            template_type = value
        data_value = data[key]
        if not isinstance(data_value, template_type):
            raise TypeError(f'Mismatching data type for {key}. \n \
Expected type {template_type.__name__} -> Received {type(data_value)}')


def validate_recursion(data, template, path):
    check_keys(data, template, path)
    check_data_type(data, template, path)

    dict_type_keys = {key for key, value in template.items() if isinstance(value, dict)}
    for key in dict_type_keys:
        sub_path = path + '.' + str(key)
        sub_template = template[key]
        sub_data = data[key]
        validate_recursion(sub_data, sub_template, sub_path)


def validate(data, template):
    validate_recursion(data, template, '')


# Inputs

template = {
    'user_id': int,
    'name': {
        'first': str,
        'last': str
    },
    'bio': {
        'dob': {
            'year': int,
            'month': int,
            'day': int
        },
        'birthplace': {
            'country': str,
            'city': str
        }
    }
}

eric = {
    'user_id': 101,
    'name': {
        'first': 'Eric',
        'last': 'Idle'
    },
    'bio': {
        'dob': {
            'year': 1943,
            'month': 3,
            'day': 29
        },
        'birthplace': {
            'country': 'United Kingdom'
        }
    }
}


michael = {
    'user_id': 102,
    'name': {
        'first': 'Michael',
        'last': 'Palin'
    },
    'bio': {
        'dob': {
            'year': 1943,
            'month': 'May',
            'day': 5
        },
        'birthplace': {
            'country': 'United Kingdom',
            'city': 'Sheffield'
        }
    }
}

john = {
    'user_id': 100,
    'name': {
        'first': 'John',
        'last': 'Cleese'
    },
    'bio': {
        'dob': {
            'year': 1939,
            'month': 11,
            'day': 27
        },
        'birthplace': {
            'country': 'United Kingdom',
            'city': 'Weston-super-Mare'
        }
    }
}

validate(john, template)
validate(eric, template)
validate(michael, template)

