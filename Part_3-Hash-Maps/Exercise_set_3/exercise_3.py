""" EXERCISE 3
You are given three JSON files, representing a default set of settings, and
environment specific settings. The files are included in the downloads, and
are named:

common.json    dev.json    prod.json

Your goal is to write a function that has a single argument (the environment
name) and returns the "combined" dictionary that merges the two dictionaries
together, with the environment specific settings overriding any common
settings already defined.

For simplicity, assume that the argument values are going to be the same as
the file names, without the .json extension. So for example, dev or prod.

The wrinkle: We don't want to duplicate data for the "merged" dictionary - use
ChainMap to implement this instead.
"""

import json
from pprint import pprint
from collections import ChainMap

def load_settings(env):
    with open(f'{env}.json') as f:
        settings = json.load(f)
    return settings


def recursive_chain(d1, d2):
    chain = ChainMap(d1, d2)
    for k, v in d1.items():
        if isinstance(v, dict) and k in d2:
            chain[k] = recursive_chain(d1[k], d2[k])
    return chain


def change_local_config(env):
    local_config = load_settings(env)
    common_config = load_settings('data/common')
    return recursive_chain(local_config, common_config)

pprint(change_local_config('data/dev'))
pprint(change_local_config('data/prod'))

