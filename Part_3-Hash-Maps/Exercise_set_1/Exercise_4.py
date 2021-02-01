""" EXERCISE 4
For this exercise suppose you have a web API load balanced across multiple
nodes. This API receives various requests for resources and logs each request
to some local storage. Each instance of the API is able to return a dictionary
containing the resource that was accessed (the dictionary key) and the number
of times it was requested (the associated value).

Your task here is to identify resources that have been requested on some, but
not all the servers, so you can determine if you have an issue with your load
balancer not distributing certain resource requests across all nodes.

For simplicity, we will assume that there are exactly 3 nodes in the cluster.

You should write a function that takes 3 dictionaries as arguments for node 1,
node 2, and node 3, and returns a dictionary that contains only keys that are
not found in all of the dictionaries. The value should be a list containing the
number of times it was requested in each node (the node order should match the
dictionary (node) order passed to your function). Use 0 if the resource was not
requested from the corresponding node.

Suppose your dictionaries are for logs of all the GET requests on each node:

    n1 = {'employees': 100, 'employee': 5000, 'users': 10, 'user': 100}
    n2 = {'employees': 250, 'users': 23, 'user': 230}
    n3 = {'employees': 150, 'users': 4, 'login': 1000}


Your result should then be:
    result = {'employee': (5000, 0, 0),
             'user': (100, 230, 0),
             'login': (0, 0, 1000)}
"""

def resources_requested(n1, n2, n3):
    nodes = [n1, n2, n3]
    incomplete_intersection = set()
    for i in range(-2,1):
        incomplete_intersection.add(*{key for key in nodes[i].keys()
        if not nodes[i+1].get(key) or not nodes[i+2].get(key)
        and key not in incomplete_intersection})
    resource_dict = {key : (n1.get(key, 0), n2.get(key, 0), n3.get(key, 0)) 
                    for key in incomplete_intersection}
    return resource_dict


# Testing
n1 = {'employees': 100, 'employee': 5000, 'users': 10, 'user': 100}
n2 = {'employees': 250, 'users': 23, 'user': 230}
n3 = {'employees': 150, 'users': 4, 'login': 1000}

print(resources_requested(n1, n2, n3))


# Alternative approach:
def identify(n1, n2, n3):
    union = n1.keys() | n2.keys() | n3.keys()
    intersection = n1.keys() & n2.keys() & n3.keys()
    relevant = union - intersection
    result = {key: (n1.get(key, 0),
                    n2.get(key, 0),
                    n3.get(key, 0))
              for key in relevant}
    return result